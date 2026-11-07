```python
# Hypothesis: gen_12 (edited, 128 problems) is our best broad diagnostic; summarize failure classes and look at the looping answers compactly.
rows=[json.loads(l) for l in open(W+'/gen_12.jsonl')]
print(len(rows), list(rows[0].keys()))
r=rows[0]; print({k:(str(v)[:80]) for k,v in r.items() if k not in('text','prompt')})
```