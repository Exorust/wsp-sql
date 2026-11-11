```python
ids128=[r['id'] for r in g1]
greq={"type":"generate","model":"edited","problems":ids128,"max_tokens":8192}
open(f'{W}/gen7_req.json','w').write(json.dumps(greq)); print(json.dumps(greq)[:200], len(ids128))
```