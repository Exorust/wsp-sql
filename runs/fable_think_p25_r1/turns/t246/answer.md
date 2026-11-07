```python
# Hypothesis: req13_items / req14 tell me what the last session was doing (loop analysis in answer region?).
it13=json.load(open(W+'/req13_items.json')); print(type(it13), (it13[:3] if isinstance(it13,list) else list(it13.keys())[:10]))
it12=json.load(open(W+'/req12_items.json')); print(type(it12), (it12[:3] if isinstance(it12,list) else list(it12.keys())[:10]))
r14=json.load(open(W+'/req14.json')); print({k:(v if k not in('texts','chats','problems','prompts') else (len(v), str(v[0])[:200])) for k,v in r14.items()})
gs=json.load(open(W+'/gen_sets.json')); print({k:len(v) for k,v in gs.items()})
sp=json.load(open(W+'/splits.json')); print({k:len(v) for k,v in sp.items()})
```