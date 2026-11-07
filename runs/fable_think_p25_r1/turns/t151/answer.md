```python
# Check req4.json (pass 4 request on original) to reuse the same texts for a paired edited TF pass
r4=json.load(open(W+'/req4.json'))
print({k:(len(v) if isinstance(v,list) else v) for k,v in r4.items()})
m4=json.load(open(W+'/fwd_4/meta.json')); print(m4.get('lengths')[:5], len(m4.get('lengths')), sorted(os.listdir(W+'/fwd_4')))
r4items=json.load(open(W+'/req4_items.json')); print(type(r4items), (r4items[:3] if isinstance(r4items,list) else list(r4items.items())[:3]))
B=json.load(open(W+'/setB.json')); print(type(B), len(B), B[0].keys() if isinstance(B[0],dict) else None)
print(repr(B[0]['text'][-300:]) if isinstance(B[0],dict) else repr(B[0][-300:]))
```