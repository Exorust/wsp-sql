```python
# Hypothesis: loop regions have all margins >= 2.5 nats (hard loop) — print margin distribution per loop text and the lowest-margin positions.
for k,astart,p,onset in loop_info[3:]:
    ids=ids13[k]; n=len(ids); ms=[]
    for i in range(onset+1, n):
        lp=float(tl[k,i]); alts=[float(l) for t,l in zip(tk[k,i],tkl[k,i]) if int(t)!=ids[i]]
        ms.append((lp-alts[0] if alts else 99, i))
    ms.sort(); print('text',k,'n',len(ms),'min margins',[round(m,2) for m,_ in ms[:5]],'median',round(float(np.median([m for m,_ in ms])),2))
    for m,i in ms[:3]:
        alt=[(tok.decode([int(t)]),round(float(l),2)) for t,l in zip(tk[k,i],tkl[k,i])][:4]
        print('   pos',i,repr(tok.decode(ids[i-3:i+1]))[-45:],'top',alt)
```