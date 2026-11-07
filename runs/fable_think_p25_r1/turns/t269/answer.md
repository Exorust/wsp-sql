```python
# Hypothesis: for the 16 loop texts (fwd_4 original vs fwd_5 probe B) the copied-token lp in the loop region barely changes.
li=items4['loop']; print(len(li), li[:2])
deltas=[]
for k in range(len(li)):
    sid=li[k] if isinstance(li[k],str) else li[k].get('id'); s=byid[sid]
    on=s['onset']; n=m4['lengths'][k]; a=t4[k,on:n]; b=t5[k,on:n]
    deltas.append((sid, round(float(np.nanmean(a)),3), round(float(np.nanmean(b)),3), round(float(np.nanmean(b-a)),3), round(float(np.nanmin(b-a)),2)))
for d in deltas: print(d)
```