```python
# Build the request texts (direct-answer format with gold SQL) for 100 confirm-pool problems not in test1
splits = json.load(open(f"{W}/splits.json")); gs = json.load(open(f"{W}/gen_sets.json"))
print(splits.keys(), gs.keys() if isinstance(gs,dict) else type(gs))
used = set(splits['diag']) | set(gs.get('test1', [])) | set(json.load(open(f"{W}/gen_sets_v1.json"))['test1'])
pool = [i for i in splits['confirm_pool'] if i not in used]
print(len(pool))
P = "/Users/chandu/myproj/wsp-sql/practice"
probs = {}
for line in open(f"{P}/spider_train.jsonl"):
    r = json.loads(line); probs[r['id']] = r
def schema_text(db): return open(f"{P}/schemas/{db}.sql").read()
def render_prompt(pid):
    r = probs[pid]
    return f"Database schema (SQLite):\n{schema_text(r['db'])}\n\nQuestion: {r['question']}\n\nWrite one SQLite query that answers the question. Reply with the query in a {FENCE}sql code block."
def render_direct(pid):
    r = probs[pid]
    return f"<|im_start|>user\n{render_prompt(pid)}<|im_end|>\n<|im_start|>assistant\n<think>\n</think>\n\n{FENCE}sql\n{r['gold']}\n{FENCE}<|im_end|>\n"
# check render matches texts7[0] prompt part
pr0 = render_prompt('sp2690'); print(pr0 in t0)
tf_ids = pool[:100]
texts10 = [render_direct(p) for p in tf_ids] + texts7
lens = [len(tok.encode(t).ids) for t in texts10]
print(len(texts10), sum(lens), max(lens))
req10 = {"type":"teacher_forced","model":"edited","texts":texts10,"return":{"token_logprobs":True,"topk":10}}
s = json.dumps(req10).replace(FENCE, "\\u0060\\u0060\\u0060")
open(f"{W}/req10.json","w").write(s); json.dump({"tf_ids":tf_ids}, open(f"{W}/req10_items.json","w"))
print(len(s))
```