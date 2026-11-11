```python
# Re-read gen_1: how far do answers get before looping, do they contain a SELECT / ```sql, and what's the failure class distribution
import re
G=[json.loads(l) for l in open(W+'/gen_1.jsonl')]
print(len(G), G[0].keys())
r=G[0]
for k,v in r.items():
    if isinstance(v,str): print(k, repr(v[:200]))
    else: print(k, v)
```