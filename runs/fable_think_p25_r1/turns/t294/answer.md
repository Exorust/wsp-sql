```python
# Hypothesis: gen_1 timing tells cost of a long-thinking gen pass; also get gen_12 ids for paired v3 test
d1=json.load(open(f'{W}/fwd_1.done.json')); print(d1['summary'], d1['seconds'])
ids12=[r['id'] for r in rows]; sub=ids12[:64]
acc12_sub=np.mean([rows[i]['cls']=='correct' for i in range(64)]); print('v2 acc on first 64 of gen_12:',acc12_sub, 'on all',np.mean([r['cls']=='correct' for r in rows]))
json.dump({'v3test':sub},open(f'{W}/gen_sets_v3.json','w'))
print(json.dumps(sub))
```