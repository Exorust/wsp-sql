```python
# Compare gold-SQL logprobs under proper no-think template (T1) vs eval template + immediate </think> (T2) in fwd_9 (original model)
m9=json.load(open(os.path.join(W,'tf9_meta.json'))); print({k:str(v)[:300] for k,v in m9.items()})
r9=json.load(open(os.path.join(W,'tf9_req.json'))); print(len(r9['texts']))
for i in [0,1]:
    t=r9['texts'][i]; a=t.find('<|im_start|>assistant'); print(i, S(t[a:a+120]).replace('\n','\\n'))
```