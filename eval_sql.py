"""Phase 0: text-to-SQL execution accuracy + failure classes for one model on BIRD Mini-Dev or Spider dev.

usage: python eval_sql.py --model models/Qwen3.5-0.8B --bench bird --thinking 0 --max-tokens 1024 --out runs/base_nothink
"""
import argparse, json, os, re, sqlite3, threading, time
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
BIRD = f"{ROOT}/data/bird_minidev/minidev/MINIDEV"
SPIDER = f"{ROOT}/data/spider/spider_data"


def load_bench(name, split="dev"):
    """-> list of dict(id, db, question, evidence, gold, db_path)"""
    if name == "bird":
        items = json.load(open(f"{BIRD}/mini_dev_sqlite.json"))
        return [dict(id=x["question_id"], db=x["db_id"], question=x["question"], evidence=x.get("evidence", ""),
                     gold=x["SQL"], db_path=f"{BIRD}/dev_databases/{x['db_id']}/{x['db_id']}.sqlite") for x in items]
    if name == "spider":
        f = "dev.json" if split == "dev" else "train_spider.json"
        items = json.load(open(f"{SPIDER}/{f}"))
        return [dict(id=i, db=x["db_id"], question=x["question"], evidence="", gold=x["query"],
                     db_path=f"{SPIDER}/database/{x['db_id']}/{x['db_id']}.sqlite") for i, x in enumerate(items)]
    if name == "math":  # MATH-500; db holds the subject, db_path unused
        return [dict(id=i, db=x["subject"], question=x["problem"], evidence="", gold=x["answer"], db_path="")
                for i, x in enumerate(map(json.loads, open("data/math500/test.jsonl")))]
    raise ValueError(name)


_schema_cache = {}


def schema_ddl(db_path):
    if db_path not in _schema_cache:
        con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        rows = con.execute("SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL AND name NOT LIKE 'sqlite_%'").fetchall()
        con.close()
        _schema_cache[db_path] = "\n\n".join(re.sub(r"\s+", " ", r[0]).strip() for r in rows)
    return _schema_cache[db_path]


def build_messages(item):
    if not item["db_path"]:
        return [{"role": "user", "content": item["question"] + "\n\nPut your final answer within \\boxed{}."}]
    ev = f"\nHint: {item['evidence']}" if item["evidence"] else ""
    user = (f"Database schema (SQLite):\n{schema_ddl(item['db_path'])}\n\nQuestion: {item['question']}{ev}\n\n"
            "Write one SQLite query that answers the question. Reply with the query in a ```sql code block.")
    return [{"role": "user", "content": user}]


def extract_sql(text):
    body = text.split("</think>")[-1] if "</think>" in text else text
    m = re.findall(r"```(?:sql|sqlite)?\s*(.*?)```", body, flags=re.S | re.I)
    if m:
        return m[-1].strip().rstrip(";") + ""
    m = re.search(r"\b(SELECT|WITH)\b.*", body, flags=re.S | re.I)
    return m.group(0).strip().split("\n\n")[0].rstrip(";") if m else None


def run_sql(db_path, sql, timeout=30):
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    t = threading.Timer(timeout, con.interrupt)
    t.start()
    try:
        return con.execute(sql).fetchall(), None
    except Exception as e:  # sqlite3.OperationalError etc.
        return None, f"{type(e).__name__}: {e}"
    finally:
        t.cancel(); con.close()


ERR_CLASSES = [("no_such_column", r"no such column"), ("no_such_table", r"no such table"), ("syntax", r"syntax error"),
               ("ambiguous", r"ambiguous column"), ("no_such_function", r"no such function"), ("timeout", r"interrupted"),
               ("misuse", r"misuse of|wrong number of arguments"), ]


def classify_error(msg):
    for name, pat in ERR_CLASSES:
        if re.search(pat, msg, flags=re.I):
            return name
    return "other_error"


def loop_score(text):
    """largest repeat count of any 40-char window; >=5 means the answer is looping"""
    best, seen = 0, Counter()
    for i in range(0, max(0, len(text) - 40), 20):
        seen[text[i:i + 40]] += 1
    return max(seen.values()) if seen else 0


def grade(item, text, cut):
    if not item["db_path"]:
        from math_verify import parse, verify
        # after the thinking block if there is one; a cut answer with no closing tag never counts
        body = text.split("</think>")[-1] if "</think>" in text else ("" if cut else text)
        ok = "\\boxed" in body and verify(parse("$" + item["gold"] + "$"), parse(body))
        return dict(sql=None, cut=cut, loop=loop_score(text), cls="correct" if ok else ("cut_no_answer" if cut else "wrong"))
    sql = extract_sql(text)
    rec = dict(sql=sql, cut=cut, loop=loop_score(text))
    if sql is None:
        rec["cls"] = "cut_no_sql" if cut else "no_sql"; return rec
    pred, err = run_sql(item["db_path"], sql)
    if err:
        rec["cls"], rec["err"] = classify_error(err), err[:200]; return rec
    gold, gerr = run_sql(item["db_path"], item["gold"])
    if gerr:
        rec["cls"], rec["err"] = "gold_error", gerr[:200]; return rec
    rec["cls"] = "correct" if set(pred) == set(gold) else "wrong_result"
    return rec


def mlx_guard(limit_gb=14):
    """Cap MLX's cache of freed GPU buffers at 1 GB (its default limit here is 30.4 GB and it filled 11 GB in one batch of 32)
    and exit the process if MLX memory still passes limit_gb. ps RSS does not show this memory, so the guard asks MLX."""
    import mlx.core as mx
    if getattr(mlx_guard, "on", False):
        return
    mlx_guard.on = True
    mx.set_cache_limit(1 << 30)

    def watch():
        while True:
            gb = (mx.get_active_memory() + mx.get_cache_memory()) / 2**30
            if gb > limit_gb:
                print(f"MLX memory {gb:.1f} GB > {limit_gb} GB: exiting", flush=True); os._exit(3)
            time.sleep(1)
    threading.Thread(target=watch, daemon=True).start()


def presence(penalty, im_start, skip):
    """OpenAI/vLLM presence penalty: subtract `penalty` from every token already generated in this answer.
    ponytail: own processor because mlx_lm's looks at the last 20 context tokens only. Stateless: one processor is shared by
    the batch, so the answer start is found as the last <|im_start|> plus the `skip` header tokens of the chat template."""
    import mlx.core as mx, numpy as np
    def proc(context, logits):
        c = np.array(context); gen = np.unique(c[np.flatnonzero(c == im_start)[-1] + 1 + skip:])
        if len(gen): idx = mx.array(gen); logits[:, idx] = logits[:, idx] - penalty
        return logits
    return proc


def loop_onset(text, step=1000):
    """first length (multiple of `step`) at which the text already loops, or None"""
    return next((p for p in range(step, len(text) + step, step) if loop_score(text[:p]) >= 5), None)


def generate_all(model_path, items, thinking, max_tokens, batch, temp, seed, rep_penalty=0.0, top_p=0.95, top_k=20, pres=0.0, ckpt=None):
    import mlx.core as mx
    from mlx_lm import load, batch_generate
    from mlx_lm.sample_utils import make_sampler, make_logits_processors
    mlx_guard()
    model, tok = load(model_path)
    extra = dict(logits_processors=make_logits_processors(repetition_penalty=rep_penalty)) if rep_penalty else {}
    prompts = [tok.encode(tok.apply_chat_template(build_messages(it), add_generation_prompt=True, tokenize=False,
                                                  enable_thinking=bool(thinking))) for it in items]
    sampler = make_sampler(temp=temp, top_p=top_p if temp else 0.0, top_k=top_k if temp else 0)
    if pres:
        im = tok.convert_tokens_to_ids("<|im_start|>"); last = len(prompts[0]) - 1 - prompts[0][::-1].index(im)
        extra = dict(logits_processors=[presence(pres, im, len(prompts[0]) - 1 - last)])
    for i, it in enumerate(items):  # after the presence set-up, which reads the bare header of prompts[0]
        if it.get("prefix"): prompts[i] = prompts[i] + tok.encode(it["prefix"], add_special_tokens=False)
    order = sorted(range(len(items)), key=lambda i: len(prompts[i]))  # similar lengths together
    texts, cut = [None] * len(items), [None] * len(items)
    # ponytail: the checkpoint trusts that the arguments are the same as in the interrupted run; delete the folder to change them
    if ckpt and os.path.exists(ckpt):
        for l in open(ckpt):
            try: d = json.loads(l); texts[d["i"]], cut[d["i"]] = d["text"], d["cut"]
            except ValueError: pass  # half-written last line
        print(f"  resumed {sum(x is not None for x in texts)}/{len(items)} from checkpoint", flush=True)
    t0 = time.time()
    for b in range(0, len(order), batch):
        idx = order[b:b + batch]
        if all(texts[i] is not None for i in idx): continue
        mx.random.seed(seed + b)
        r = batch_generate(model, tok, prompts=[prompts[i] for i in idx], max_tokens=max_tokens, sampler=sampler,
                           verbose=False, return_token_ids=True, **extra)
        mx.clear_cache()
        for j, i in enumerate(idx):
            texts[i] = r.texts[j]
            ids = r.token_ids[j]
            cut[i] = len(ids) >= max_tokens and (not ids or ids[-1] not in tok.eos_token_ids)
        if ckpt:
            with open(ckpt, "a") as f:
                for i in idx: f.write(json.dumps(dict(i=i, text=texts[i], cut=bool(cut[i]))) + "\n")
                f.flush(); os.fsync(f.fileno())
        done = b + len(idx)
        print(f"  {done}/{len(items)}  {time.time() - t0:.0f}s", flush=True)
    return texts, cut


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True); ap.add_argument("--bench", default="bird")
    ap.add_argument("--split", default="dev"); ap.add_argument("--thinking", type=int, default=0)
    ap.add_argument("--max-tokens", type=int, default=1024); ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--temp", type=float, default=0.0, help="0 = greedy")
    ap.add_argument("--n", type=int, default=0); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--rep-penalty", type=float, default=0.0, help="decoding-only control, e.g. 1.2")
    ap.add_argument("--top-p", type=float, default=0.95); ap.add_argument("--top-k", type=int, default=20)
    ap.add_argument("--presence", type=float, default=0.0, help="presence penalty over the whole answer; the report uses 1.5")
    ap.add_argument("--prefix-from", help="results.jsonl of a looping run: continue each looping answer from the point where its loop is established")
    ap.add_argument("--prefix-n", type=int, default=60)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    items = load_bench(a.bench, a.split)
    if a.n:
        items = items[::max(1, len(items) // a.n)][:a.n]  # evenly spaced, so every database is represented
    if a.prefix_from:
        src = {r["id"]: r for r in map(json.loads, open(a.prefix_from))}; keep = []
        for it in items:
            r = src.get(it["id"]); p = r and r["cut"] and "</think>" not in r["text"] and loop_onset(r["text"])
            if p: keep.append(dict(it, prefix=r["text"][:p]))
        items = keep[:a.prefix_n]
    os.makedirs(a.out, exist_ok=True)
    texts, cut = generate_all(a.model, items, a.thinking, a.max_tokens, a.batch, a.temp, a.seed, a.rep_penalty, a.top_p, a.top_k, a.presence,
                              ckpt=f"{a.out}/partial.jsonl")
    recs = []
    with open(f"{a.out}/results.jsonl", "w") as f:
        for it, tx, c in zip(items, texts, cut):
            rec = dict(id=it["id"], db=it["db"], **grade(it, tx, c), text=tx, **({"prefix_chars": len(it["prefix"])} if it.get("prefix") else {}))
            recs.append(rec); f.write(json.dumps(rec) + "\n")
    n = len(recs)
    cls = Counter(r["cls"] for r in recs)
    summ = dict(model=a.model, bench=a.bench, split=a.split, thinking=a.thinking, max_tokens=a.max_tokens, temp=a.temp, rep_penalty=a.rep_penalty, top_p=a.top_p, top_k=a.top_k, presence=a.presence, seed=a.seed,
                n=n, acc=cls["correct"] / n, cut_share=sum(r["cut"] for r in recs) / n,
                loop_share=sum(r["loop"] >= 5 for r in recs) / n, classes={k: v / n for k, v in cls.most_common()},
                err_detail=Counter(r.get("err", "")[:60] for r in recs if "err" in r).most_common(15))
    json.dump(summ, open(f"{a.out}/summary.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in summ.items() if k != "err_detail"}, indent=1))


if __name__ == "__main__":
    main()
