```python
# Retry printing (previous block printed nothing - maybe an exception swallowed?). Simplify.
out=[]
for i,(kind,pid) in enumerate(kinds9):
    ids=ids9[i]; pos=ids.index(248068); pth=ids.index(TH)
    pf=[p for p in range(pth,len(ids)) if ids[p]==71093]
    body=list(range(pf[0]+3, pf[1]))
    out.append((kind,pid, repr(tok.decode([ids[pos+1]]))[:6], round(float(lp9[i,pos+1]),2), round(float(lp9[i,pth]),2), [round(float(lp9[i,p]),2) for p in range(pth+1,pth+5)], round(float(np.mean(lp9[i,body])),3), round(float(np.sum(lp9[i,body])),1), len(body)))
for o in out: print(o)
```