```python
# Verify alignment and gather model predictions at the decision positions
kw={k:enc(k) for k in [' JOIN',' WHERE',' GROUP',' ORDER',' DISTINCT','\n',' AS',' LIMIT',' HAVING',' INTERSECT',' UNION',' EXCEPT',' ,',',',' LEFT',' INNER',' ON',' count',' COUNT',' *',' T']}
print({k:v for k,v in kw.items()})
# alignment check: topk at starts-1 should predict SELECT (ids[starts])
sel_id=enc('SELECT')[0]
print('alignment check:', [tk12[i,starts[i]-1,0]==T12[i][starts[i]] for i in range(5)], [tk12[i,starts[i],0]==T12[i][starts[i]] for i in range(5)])
```