```python
# Shrink the request: 30 shortest-prompt problems from the pool + fwd_7 texts 0,4,5
pool_sorted = sorted(pool, key=lambda p: len(render_prompt(p)))
tf_ids = pool_sorted[:30]
texts10 = [render_direct(p) for p in tf_ids] + [texts7[0], texts7[4], texts7[5]]
lens = [len(tok.encode(t).ids) for t in texts10]
req10 = {"type":"teacher_forced","model":"edited","texts":texts10,"return":{"token_logprobs":True,"topk":10}}
s = json.dumps(req10).replace(FENCE, "\\u0060\\u0060\\u0060")
open(f"{W}/req10.json","w").write(s); json.dump({"tf_ids":tf_ids}, open(f"{W}/req10_items.json","w"))
print(len(texts10), sum(lens), max(lens), len(s))
```