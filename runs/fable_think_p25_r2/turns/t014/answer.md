```python
# Hypothesis: gen_1.jsonl holds the diagnostic generation; summarize grades/failure classes
import collections
rows=[json.loads(l) for l in open(W+'/gen_1.jsonl')]
print(len(rows)); print(list(rows[0].keys()))
print(json.load(open(W+'/fwd_1.done.json')) if os.path.getsize(W+'/fwd_1.done.json')<3000 else 'big')
r=rows[0]
for k,v in r.items():
    s=str(v); print(k,':',s[:200].replace('\n','\\n'))
```