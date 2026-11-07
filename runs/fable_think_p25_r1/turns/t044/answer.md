```python
# Inspect gen_1: how do the looping answers look? where does the loop start, what repeats?
import collections
rows = [json.loads(l) for l in open(W+"/gen_1.jsonl")]
print(len(rows), list(rows[0].keys()))
r = rows[0]
for k,v in r.items():
    if isinstance(v,str): print(k, len(v), repr(v[:200]))
    else: print(k, v if not isinstance(v,(list,dict)) else type(v))
```