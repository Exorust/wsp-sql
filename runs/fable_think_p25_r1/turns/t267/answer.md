```python
# Hypothesis: compute, for the 16 loop texts, mean lp of tokens in the loop region (after onset) under original (fwd_4) vs probe B (fwd_5); little change would mean heads aren't the copy mechanism.
byid={s['id']:s for s in setA}
items4=json.load(open(W+'/req4_items.json')); print(items4[:2])
deltas=[]
for k in range(16):
    it=items4[k]; s=byid.get(it['id'] if isinstance(it,dict) else it)
    if s is None: continue
    ids=tok.encode(tx4[k]).ids; on=s['onset']; n=m4['lengths'][k]
    a=t4[k,on:n]; b=t5[k,on:n]
    deltas.append((float(np.nanmean(a)),float(np.nanmean(b)),float(np.nanmean(b-a)), float(np.nanmin(b-a))))
for d in deltas[:16]: print([round(x,3) for x in d])
```