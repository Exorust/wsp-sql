```python
print(type(setB[0]), (setB[0].keys() if isinstance(setB[0],dict) else setB[0][:300]))
b = setB[0]
for k,v in b.items():
    print(k, repr(v)[:300] if not isinstance(v,str) else repr(v[-400:]))
print([len(t) for t in req3['texts']][:5], sum(len(tok.encode(t).ids) for t in req3['texts'][:20])/20)
```