"""Forward-pass tool: generation (graded by SQL execution; "both" = paired original vs edited) and teacher-forced reads
(log-probs, hidden states, MLP activations, attention). mlx-lm generates; transformers (MPS) reads activations.
Edits (work/edited/*.npy, float32) are cast to bfloat16 into a rebuilt safetensors file at work/edited_model/."""
import hashlib, json, os, shutil, sys, time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from eval_sql import SPIDER, build_messages, grade, loop_score, mlx_guard

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_CFG = dict(thinking=False, max_tokens=1024, temp=0.0, gen_max=512, tf_max_texts=1024, tf_max_tokens=8192,
                   tf_total_tokens=524_288, act_max_tokens=2048, batch=16, attn_max_texts=2, attn_max_tokens=2048)


class Forward:
    def __init__(self, base_dir, work, practice_jsonl, cfg=None):
        self.base, self.work = os.path.abspath(base_dir), os.path.abspath(work)
        self.cfg = dict(DEFAULT_CFG, **(cfg or {}))
        self.practice = {}
        for line in open(practice_jsonl):
            it = json.loads(line)
            it["db_path"] = f"{SPIDER}/database/{it['db']}/{it['db']}.sqlite"; it["evidence"] = ""
            self.practice[it["id"]] = it
        self._mlx, self._hf = {}, {}
        self._edit_sig = None

    # ---------- models ----------
    def edit_manifest(self):
        d = f"{self.work}/edited"
        names = sorted(f[:-4] for f in os.listdir(d)) if os.path.isdir(d) else []
        sig = hashlib.sha1("".join(f"{n}:{os.path.getmtime(f'{d}/{n}.npy')}" for n in names).encode()).hexdigest()
        return names, sig

    def build_edited(self):
        """rebuild work/edited_model from base + edits (bf16). -> list of edited tensor names"""
        import torch
        from safetensors.torch import load_file, save_file
        names, sig = self.edit_manifest()
        out = f"{self.work}/edited_model"
        if sig == self._edit_sig and os.path.isdir(out):
            return names
        shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
        for f in os.listdir(self.base):
            if not f.endswith(".safetensors"):
                os.symlink(f"{self.base}/{f}", f"{out}/{f}")
        st = f"{self.base}/model.safetensors-00001-of-00001.safetensors"
        tensors = load_file(st)
        for n in names:
            t = torch.from_numpy(np.load(f"{self.work}/edited/{n}.npy")).to(torch.bfloat16)
            assert t.shape == tensors[n].shape, n
            tensors[n] = t
        save_file(tensors, f"{out}/model.safetensors-00001-of-00001.safetensors", metadata={"format": "pt"})
        json.dump(dict(edited=names, sig=sig), open(f"{out}/EDIT_MANIFEST.json", "w"))
        self._edit_sig = sig
        self._mlx.pop("edited", None); self._hf.pop("edited", None)
        return names

    def model_dir(self, which):
        return self.base if which == "original" else f"{self.work}/edited_model"

    def mlx(self, which):
        if which not in self._mlx:
            import mlx.core as mx
            from mlx_lm import load
            mlx_guard()
            self._mlx[which] = load(self.model_dir(which))
        return self._mlx[which]

    def free(self):
        """drop every loaded model and the Metal cache (called after each pass; the laptop has 32 GB)"""
        import gc
        self._mlx.clear(); self._hf.clear(); gc.collect()
        try:
            import mlx.core as mx; mx.clear_cache()
        except Exception:
            pass
        try:
            import torch; torch.mps.empty_cache()
        except Exception:
            pass

    def hf(self, which, eager=False):
        key = (which, eager)
        if key not in self._hf:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
            kw = dict(attn_implementation="eager") if eager else {}
            m = AutoModelForCausalLM.from_pretrained(self.model_dir(which), dtype=torch.bfloat16, device_map="mps", **kw).eval()
            self._acts = {}
            for n, mod in m.named_modules():
                if n.endswith("mlp.down_proj"):
                    i = int(n.split("layers.")[1].split(".")[0])
                    mod.register_forward_hook(lambda mod, inp, out, i=i: self._acts.__setitem__(i, inp[0][0].detach().float().cpu().numpy()))
            self._hf[key] = (m, AutoTokenizer.from_pretrained(self.base))
        return self._hf[key]

    # ---------- requests ----------
    def handle(self, req, k):
        """-> (summary_text, counted: bool)"""
        try:
            if req.get("type") == "generate":
                return self.generate(req, k), True
            if req.get("type") == "teacher_forced":
                return self.teacher_forced(req, k), True
            return f'request failed (not counted): unknown "type" {req.get("type")!r}', False
        except AssertionError as e:
            return f"request failed (not counted): {e}", False
        finally:
            self.free()

    def _prompt_ids(self, tok, item=None, user=None):
        msgs = build_messages(item) if item is not None else [{"role": "user", "content": user}]
        return tok.encode(tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False,
                                                  enable_thinking=bool(self.cfg["thinking"])))

    def _gen_one_model(self, which, items, prompts_ids, max_tokens, seeds):
        import mlx.core as mx
        from mlx_lm import batch_generate
        from mlx_lm.sample_utils import make_sampler
        model, tok = self.mlx(which)
        temp = self.cfg["temp"]
        sampler = make_sampler(temp=temp, top_p=0.95 if temp else 0.0, top_k=20 if temp else 0)
        B = self.cfg["batch"]; recs = [None] * len(items)
        order = sorted(range(len(items)), key=lambda i: len(prompts_ids[i]))
        for b in range(0, len(order), B):
            idx = order[b:b + B]
            mx.random.seed(seeds[idx[0]])
            r = batch_generate(model, tok, prompts=[prompts_ids[i] for i in idx], max_tokens=max_tokens, sampler=sampler,
                               verbose=False, return_token_ids=True)
            mx.clear_cache()
            for j, i in enumerate(idx):
                ids = r.token_ids[j]
                cut = len(ids) >= max_tokens and (not ids or ids[-1] not in tok.eos_token_ids)
                it = items[i]
                if it["item"] is not None:
                    g = grade(it["item"], r.texts[j], cut)
                else:
                    g = dict(sql=None, cut=cut, loop=loop_score(r.texts[j]), cls="ungraded")
                recs[i] = dict(id=it["id"], db=it["item"]["db"] if it["item"] else None, n_tokens=len(ids), **g, text=r.texts[j])
        return recs

    def _acts_for(self, which, recs, prompts_ids, layers, mlp, out_dir):
        """residual at last prompt token + mean over answer tokens (first act_max_tokens) for requested layers"""
        import torch
        m, tok = self.hf(which)
        os.makedirs(out_dir, exist_ok=True)
        last, mean, mlpm, index = [], [], [], []
        for rec, pid in zip(recs, prompts_ids):
            aid = tok(rec["text"], add_special_tokens=False)["input_ids"][: self.cfg["act_max_tokens"]]
            ids = torch.tensor([list(pid) + aid], device="mps")
            with torch.no_grad():
                o = m(input_ids=ids, output_hidden_states=True)
            hs = [o.hidden_states[l][0].float().cpu().numpy() for l in layers]
            P = len(pid)
            last.append(np.stack([h[P - 1] for h in hs])); mean.append(np.stack([h[P:].mean(0) if len(aid) else h[P - 1] for h in hs]))
            if mlp:
                mlpm.append(np.stack([self._acts[l][P:].mean(0) if len(aid) and l in self._acts else np.zeros(3584, np.float32) for l in layers]))
            index.append(dict(id=rec["id"], cls=rec["cls"], correct=rec["cls"] == "correct", n_answer_tokens=len(aid)))
        np.save(f"{out_dir}/resid_last_prompt.npy", np.stack(last).astype(np.float16))
        np.save(f"{out_dir}/resid_answer_mean.npy", np.stack(mean).astype(np.float16))
        if mlp:
            np.save(f"{out_dir}/mlp_down_in_answer_mean.npy", np.stack(mlpm).astype(np.float16))
        json.dump(dict(layers=layers, files=sorted(os.listdir(out_dir)), shape_note="[n_items, n_layers, dim]; layers index 0 = embeddings",
                       samples=index), open(f"{out_dir}/index.json", "w"))

    @staticmethod
    def _summ(recs):
        n = len(recs); graded = [r for r in recs if r["cls"] != "ungraded"]
        from collections import Counter
        cls = Counter(r["cls"] for r in recs)
        s = dict(n=n, accuracy=round(sum(r["cls"] == "correct" for r in graded) / max(1, len(graded)), 4),
                 mean_tokens=round(sum(r["n_tokens"] for r in recs) / n, 1), cut_at_max_tokens=cls_share(recs, "cut"),
                 looping=round(sum(r["loop"] >= 5 for r in recs) / n, 4), failures={k: v for k, v in cls.most_common() if k != "correct"})
        return s

    def generate(self, req, k):
        which = req.get("model", "original"); assert which in ("original", "edited", "both"), "model must be original/edited/both"
        n = int(req.get("n", 1)); assert n >= 1
        max_tokens = int(req.get("max_tokens", self.cfg["max_tokens"])); assert 1 <= max_tokens <= self.cfg["max_tokens"] * 8
        probs = req.get("problems", []); prompts = req.get("prompts", [])
        for p in probs:
            assert p in self.practice, f"unknown practice id {p!r}"
        items = [dict(id=p, item=self.practice[p]) for p in probs] + [dict(id=f"prompt{i}", item=None, user=u) for i, u in enumerate(prompts)]
        assert items, "no problems or prompts"
        items = [dict(it, id=f"{it['id']}#{s}" if n > 1 else it["id"]) for it in items for s in range(n)]
        cap = self.cfg["gen_max"] // (2 if which == "both" else 1)
        assert len(items) <= cap, f"{len(items)} generations > limit {cap} for model={which}"
        edited_names = self.build_edited() if which != "original" else []
        if which != "original":
            assert edited_names, "no edits saved yet (save_edit first) - 'edited' would equal 'original'"
        _, tok = self.mlx("original")
        prompts_ids = [self._prompt_ids(tok, it["item"], it.get("user")) for it in items]
        seeds = [int(hashlib.sha1(it["id"].encode()).hexdigest()[:8], 16) for it in items]
        acts = req.get("activations")
        t0 = time.time(); out = dict(pass_id=k, type="generate", model=which, max_tokens=max_tokens)
        models = ["original", "edited"] if which == "both" else [which]
        results = {}
        for w in models:
            recs = self._gen_one_model(w, items, prompts_ids, max_tokens, seeds)
            results[w] = recs
            fn = f"{self.work}/gen_{k}.jsonl" if which != "both" else f"{self.work}/gen_{k}_{w}.jsonl"
            with open(fn, "w") as f:
                for r in recs:
                    f.write(json.dumps(r) + "\n")
            out[w if which == "both" else "summary"] = self._summ(recs); out.setdefault("files", []).append(fn)
            if acts:
                layers = [int(l) for l in acts.get("layers", [])]; assert all(0 <= l <= 24 for l in layers), "layers in 0..24"
                d = f"{self.work}/gen_{k}_acts" + (f"/{w}" if which == "both" else "")
                self._acts_for(w, recs, prompts_ids, layers, bool(acts.get("mlp")), d)
                out.setdefault("activation_dirs", []).append(d)
        if which == "both":
            o, e = results["original"], results["edited"]
            graded = [(a["cls"] == "correct", b["cls"] == "correct") for a, b in zip(o, e) if a["cls"] != "ungraded"]
            if graded:
                d = np.array([float(b) - float(a) for a, b in graded])
                out["paired"] = dict(n=len(d), acc_diff_edited_minus_original=round(float(d.mean()), 4),
                                     standard_error=round(float(d.std(ddof=1) / np.sqrt(len(d))), 4) if len(d) > 1 else None,
                                     wrong_to_right=int(sum(1 for a, b in graded if b and not a)),
                                     right_to_wrong=int(sum(1 for a, b in graded if a and not b)))
            out["edited_tensors"] = edited_names
        out["seconds"] = round(time.time() - t0)
        json.dump(out, open(f"{self.work}/fwd_{k}.done.json", "w"), indent=1)
        return json.dumps(out, indent=1)

    def teacher_forced(self, req, k):
        import torch
        which = req.get("model", "original"); assert which in ("original", "edited"), "model must be original or edited"
        if which == "edited":
            assert self.build_edited(), "no edits saved yet"
        ret = req.get("return", {}); assert ret, '"return" is required'
        texts, chats = req.get("texts"), req.get("chats")
        assert (texts or chats) and not (texts and chats), 'give "texts" or "chats"'
        attn_layers = ret.get("attn_layers")
        m, tok = self.hf(which, eager=bool(attn_layers))
        if chats:
            texts = [tok.apply_chat_template(c, tokenize=False, add_generation_prompt=False, enable_thinking=bool(req.get("enable_thinking", False))) for c in chats]
        assert len(texts) <= self.cfg["tf_max_texts"], f"at most {self.cfg['tf_max_texts']} texts"
        if attn_layers:
            assert len(texts) <= self.cfg["attn_max_texts"], f"attn_layers: at most {self.cfg['attn_max_texts']} texts"
        enc = [tok(t, add_special_tokens=False)["input_ids"][: self.cfg["tf_max_tokens"]] for t in texts]
        total = sum(len(e) for e in enc); assert total <= self.cfg["tf_total_tokens"], f"{total} tokens > {self.cfg['tf_total_tokens']}"
        hs_layers = [int(l) for l in ret.get("hidden_states", [])]; mlp_layers = [int(l) for l in ret.get("mlp_act", [])]
        T = max(len(e) for e in enc); N = len(enc)
        est = N * T * (2 * (len(hs_layers) * 1024 + len(mlp_layers) * 3584) + 4 * (1 + 8 * int(ret.get("topk", 0))))
        assert est <= 6 << 30, f"result would be ~{est / 2**30:.1f} GB > 6 GB; ask for fewer texts/layers"
        d = f"{self.work}/fwd_{k}"; os.makedirs(d, exist_ok=True)
        lp = np.full((N, T), np.nan, np.float32) if ret.get("token_logprobs") else None
        topk = int(ret.get("topk", 0)); assert topk <= 50
        tk_ids = np.zeros((N, T, topk), np.int32) if topk else None; tk_lp = np.zeros((N, T, topk), np.float32) if topk else None
        hs = {l: np.zeros((N, T, 1024), np.float16) for l in hs_layers}; ma = {l: np.zeros((N, T, 3584), np.float16) for l in mlp_layers}
        attn = {}
        t0 = time.time()
        for i, ids in enumerate(enc):
            x = torch.tensor([ids], device="mps")
            with torch.no_grad():
                o = m(input_ids=x, output_hidden_states=bool(hs_layers), output_attentions=bool(attn_layers))
            L = len(ids)
            if lp is not None or topk:
                logp = torch.log_softmax(o.logits[0].float(), -1)
                if lp is not None and L > 1:
                    lp[i, 1:L] = logp[:-1].gather(1, x[0, 1:, None]).squeeze(1).cpu().numpy()
                if topk:
                    v, ix = logp.topk(topk, -1); tk_ids[i, :L] = ix.cpu().numpy(); tk_lp[i, :L] = v.cpu().numpy()
            for l in hs_layers:
                hs[l][i, :L] = o.hidden_states[l][0].float().cpu().numpy()
            for l in mlp_layers:
                ma[l][i, :L] = self._acts[l]
            if attn_layers and o.attentions:
                FULL = [3, 7, 11, 15, 19, 23]
                for l in attn_layers:
                    a = o.attentions[FULL.index(l)] if l in FULL else None
                    if a is not None:
                        attn.setdefault(l, []).append(a[0].float().cpu().numpy().astype(np.float16))
        files = []
        if lp is not None: np.save(f"{d}/token_logprobs.npy", lp); files.append("token_logprobs.npy [N,T] (nan at position 0 / padding)")
        if topk: np.save(f"{d}/topk_ids.npy", tk_ids); np.save(f"{d}/topk_logprobs.npy", tk_lp); files += ["topk_ids.npy [N,T,k]", "topk_logprobs.npy [N,T,k]"]
        for l in hs_layers: np.save(f"{d}/hidden_L{l}.npy", hs[l]); files.append(f"hidden_L{l}.npy [N,T,1024] float16")
        for l in mlp_layers: np.save(f"{d}/mlp_down_in_L{l}.npy", ma[l]); files.append(f"mlp_down_in_L{l}.npy [N,T,3584] float16 (down_proj input)")
        for l, arrs in attn.items():
            for i, a in enumerate(arrs): np.save(f"{d}/attn_L{l}_text{i}.npy", a); files.append(f"attn_L{l}_text{i}.npy [heads,T,T]")
        if attn_layers and not attn: files.append("(no attention weights returned for the requested layers: only full-attention layers 3,7,11,15,19,23 have them)")
        meta = dict(pass_id=k, type="teacher_forced", model=which, n_texts=N, lengths=[len(e) for e in enc], max_len=T,
                    files=files, dir=d, seconds=round(time.time() - t0))
        json.dump(meta, open(f"{d}/meta.json", "w"), indent=1)
        json.dump(meta, open(f"{self.work}/fwd_{k}.done.json", "w"), indent=1)
        return json.dumps(meta, indent=1)


def cls_share(recs, key):
    return round(sum(bool(r.get(key)) for r in recs) / max(1, len(recs)), 4)


if __name__ == "__main__":  # self-check: tiny generate both + teacher-forced
    import tempfile
    work = tempfile.mkdtemp(); print("work", work)
    fw = Forward(f"{ROOT}/models/Qwen3.5-0.8B", work, f"{ROOT}/practice/spider_train.jsonl", dict(batch=8))
    ids = list(fw.practice)[:8]
    print(fw.handle({"type": "generate", "model": "original", "problems": ids, "activations": {"layers": [15, 19], "mlp": True}}, 1)[0][:1500])
    os.makedirs(f"{work}/edited"); W = np.load if False else None
    from safetensors.torch import load_file
    import torch
    t = load_file(f"{ROOT}/models/Qwen3.5-0.8B/model.safetensors-00001-of-00001.safetensors")["model.language_model.layers.15.mlp.down_proj.weight"].float()
    t[:, :64] *= 0.9; np.save(f"{work}/edited/model.language_model.layers.15.mlp.down_proj.weight.npy", t.numpy())
    print(fw.handle({"type": "generate", "model": "both", "problems": ids}, 2)[0][:1500])
    print(fw.handle({"type": "teacher_forced", "model": "original", "chats": [[{"role": "user", "content": "hi"}, {"role": "assistant", "content": "SELECT 1"}]],
                     "return": {"token_logprobs": True, "topk": 5, "hidden_states": [15], "mlp_act": [15], "attn_layers": [15]}}, 3)[0])
    print(fw.handle({"type": "generate", "model": "both", "problems": ids * 100}, 4))
    import mlx.core as mx
    assert mx.get_cache_memory() <= 1.1 * 2**30 and not fw._mlx, "models or GPU buffers left behind after a pass"
    print("forward self-check OK")
