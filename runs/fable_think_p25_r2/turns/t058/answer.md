```python
print(len(G)); print(list(G[0].keys()))
r=G[0]
for k,v in r.items():
    if isinstance(v,str): print(k, repr(v[:200]))
    else: print(k, str(v)[:200])
```