```python
# Pick 48 unused problems from confirm_pool for paired generation test of v1
sp=json.load(open(W+'/splits.json')); print(sp.keys(), len(sp['confirm_pool']))
used=set(sp['diag'])|set(g['id'] for g in g6o)
pool=[i for i in sp['confirm_pool'] if i not in used]
rng=np.random.RandomState(8); test1=list(rng.choice(pool,48,replace=False))
json.dump({'test1':test1},open(W+'/gen_sets_v1.json','w'))
print(json.dumps({"type":"generate","model":"both","problems":test1,"max_tokens":8192}))
```