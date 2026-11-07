```python
# Final small TF request: 8 shortest direct-format texts
tf_ids = pool_sorted[:8]
texts10 = [render_direct(p) for p in tf_ids]
req10 = {"type":"teacher_forced","model":"edited","texts":texts10,"return":{"token_logprobs":True,"topk":10}}
s = json.dumps(req10).replace(FENCE, "\\u0060\\u0060\\u0060")
open(f"{W}/req10.json","w").write(s); json.dump({"tf_ids":tf_ids}, open(f"{W}/req10_items.json","w"))
print(len(s)); print(s)
```