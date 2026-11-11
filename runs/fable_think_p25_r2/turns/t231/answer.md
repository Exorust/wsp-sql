```python
# debug SQL start detection
i=3
ids=tok.encode(texts[i]).ids; toks=[tok.decode([t]) for t in ids]
s=texts[i].rfind(FENCE+'sql\n'); pos=0; start=None
for j,t in enumerate(toks):
    pos+=len(t)
    if start is None and pos>s+7: start=j
print(start, [S(repr(t)) for t in toks[start-3:start+8]])
print('n res', len(res))
```