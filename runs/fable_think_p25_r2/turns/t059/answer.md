```python
import json, re
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r2/work'
G=[json.loads(l) for l in open(W+'/gen_1.jsonl')]
print(len(G)); print(list(G[0].keys()))
r=G[0]
for k,v in r.items():
    if isinstance(v,str): print(k, repr(v[:200]))
    else: print(k, str(v)[:200])
```