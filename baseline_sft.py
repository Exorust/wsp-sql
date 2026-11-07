"""Same-footprint gradient baseline: fine-tune ONLY the weight entries an agent changed (mask = base != edited checkpoint),
with plain next-token loss on gold SQL from Spider train. Output is a model folder for eval_sql.py.

usage: python baseline_sft.py --footprint models/Qwen3.5-0.8B-weight-space-programming --n 500 --steps 125 --out runs/sft_mathloci
       python baseline_sft.py --footprint runs/wsp_p25/work/edited_model ...   (an agent's SQL edit as the footprint)
ponytail: SQL only (gold answers exist); the math arena needs a self-distillation data step first.
"""
import argparse, json, os, sys, time
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT); sys.path.insert(0, f"{ROOT}/harness")
from eval_sql import load_bench, build_messages

ST = "model.safetensors-00001-of-00001.safetensors"


def footprint(base, edited):
    """-> {safetensors name: bool mask of changed entries}"""
    from safetensors import safe_open
    import torch
    a, b = safe_open(f"{base}/{ST}", "pt"), safe_open(f"{edited}/{ST}", "pt")
    out = {}
    for n in a.keys():
        x, y = a.get_tensor(n), b.get_tensor(n)
        if not torch.equal(x, y):
            out[n] = (x != y).numpy()
    assert out, "footprint is empty: the two checkpoints are identical"
    return out


def hf_name(st_name):  # safetensors "model.language_model.X" -> transformers "model.X"
    assert st_name.startswith("model.language_model."), st_name
    return "model." + st_name[len("model.language_model."):]


def examples(tok, items, thinking=False):
    """-> list of (token ids, number of prompt tokens); the loss covers only the completion (```sql ... ``` + end token)"""
    out = []
    for it in items:
        p = tok.apply_chat_template(build_messages(it), add_generation_prompt=True, tokenize=False, enable_thinking=thinking)
        # thinking on: the prompt ends with "<think>\n"; the target closes thinking at once, the same behaviour the agent's edit produced
        pid = tok.encode(p); cid = tok.encode(("</think>\n\n" if thinking else "") + f"```sql\n{it['gold']}\n```") + [tok.convert_tokens_to_ids("<|im_end|>")]
        out.append((pid + cid, len(pid)))
    return out


def train(base, masks, exs, steps, lr, batch, seed, log):
    """torch on MPS: the MLX model's linear-attention kernel has no backward pass, and its ops fallback needs >14 GB"""
    import torch
    from transformers import AutoModelForCausalLM
    torch.manual_seed(seed)
    model = AutoModelForCausalLM.from_pretrained(base, dtype=torch.float32, device_map="mps")  # float32 everywhere: 3.2 GB, and no mixed-dtype matmuls
    model.train(); model.requires_grad_(False)
    params = dict(model.named_parameters()); names = {hf_name(n): n for n in masks}
    tmask = {}
    for k, n in names.items():
        p = params[k]; p.requires_grad_(True)
        tmask[k] = torch.from_numpy(masks[n]).to("mps")
        p.register_hook(lambda g, m=tmask[k]: g * m)  # gradient only inside the footprint
    opt = torch.optim.Adam([params[k] for k in names], lr=lr)
    rng = np.random.default_rng(seed); t0 = time.time()
    for s in range(steps):
        idx = rng.choice(len(exs), batch, replace=False)
        L = max(len(exs[i][0]) for i in idx)
        ids = torch.tensor([exs[i][0] + [0] * (L - len(exs[i][0])) for i in idx], device="mps")
        h = model.model(input_ids=ids).last_hidden_state  # logits only at completion positions: full [B, L, 248k] logits need >3 GB
        loss, ntok = 0.0, 0
        for r, i in enumerate(idx):
            a, b = exs[i][1], len(exs[i][0])
            loss = loss + torch.nn.functional.cross_entropy(model.lm_head(h[r, a - 1 : b - 1]).float(), ids[r, a:b], reduction="sum"); ntok += b - a
        loss = loss / ntok
        opt.zero_grad(); loss.backward(); opt.step(); torch.mps.empty_cache()
        if s % 10 == 0 or s == steps - 1:
            msg = f"step {s} loss {loss.item():.4f} {time.time() - t0:.0f}s"; print(msg, flush=True); log.write(msg + "\n")
    return {n: params[k].detach().float().cpu().numpy() for k, n in names.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=f"{ROOT}/models/Qwen3.5-0.8B"); ap.add_argument("--footprint", required=True, help="edited checkpoint folder; mask = entries that differ from --model")
    ap.add_argument("--n", type=int, default=500); ap.add_argument("--steps", type=int, default=125); ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--lr", type=float, default=2e-4); ap.add_argument("--seed", type=int, default=0); ap.add_argument("--out", required=True)
    ap.add_argument("--thinking", type=int, default=0, help="1: thinking template, target = </think> then the SQL")
    a = ap.parse_args()
    os.makedirs(f"{a.out}/edited", exist_ok=True)
    masks = footprint(a.model, a.footprint)
    print({n: int(m.sum()) for n, m in masks.items()}, "trainable entries")
    from mlx_lm import load
    _, tok = load(a.model)
    items = load_bench("spider", "train"); rng = np.random.default_rng(a.seed); items = [items[i] for i in rng.permutation(len(items))[: a.n]]
    exs = [x for x in examples(tok, items, bool(a.thinking)) if len(x[0]) <= 1024]  # ponytail: the reference linear-attention backward needs >14 GB on longer rows
    print(len(exs), 'examples of at most 1,024 tokens')
    with open(f"{a.out}/train.log", "a") as log:
        trained = train(a.model, masks, exs, a.steps, a.lr, a.batch, a.seed, log)
    from safetensors import safe_open
    base = safe_open(f"{a.model}/{ST}", "pt")
    for n, w in trained.items():
        o = base.get_tensor(n).float().numpy()
        w = np.where(masks[n], w, o)  # belt and braces: outside the footprint stays exactly the base
        np.save(f"{a.out}/edited/{n}.npy", w)
        print(n, "changed entries", int((w != o).sum()), "max |delta|", float(np.abs(w - o).max()))
    from forward import Forward
    Forward(a.model, a.out, f"{ROOT}/practice/spider_train.jsonl").build_edited()
    json.dump(vars(a) | dict(footprint_entries={n: int(m.sum()) for n, m in masks.items()}), open(f"{a.out}/sft_meta.json", "w"), indent=1)
    print("model at", f"{a.out}/edited_model")


if __name__ == "__main__":
    main()
