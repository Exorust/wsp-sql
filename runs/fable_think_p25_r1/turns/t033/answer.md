```python
# Redo: distribution predicting token t is tk[:, t-1]. Track p(NL) vs p(NL2) vs other at bullet-ends
def dist_at(ti, t):
    return {int(i):float(l) for i,l in zip(tk[ti,t-1],tlp[ti,t-1])}
for ti in range(2):
    ids=np.array(toks[ti]); T=len(ids)
    print("text",ti)
    for t in eol_positions(ids):
        if t<560 and ti==1: continue
        if t<245 and ti==0: continue
        d=dist_at(ti,t)
        p1=np.exp(d.get(NL,-30)); p2=np.exp(d.get(NL2,-30))
        others=[(tok.decode([k]).replace('\n','\\n'),round(np.exp(v),3)) for k,v in d.items() if k not in (NL,NL2)][:3]
        prev=tok.decode(ids[max(0,t-5):t]).replace('\n','\\n')
        print(f"t={t:4d} actual={'NL ' if ids[t]==NL else 'NL2'} p(NL)={p1:.3f} p(NL2)={p2:.3f} others={others} prev={prev!r}")
```