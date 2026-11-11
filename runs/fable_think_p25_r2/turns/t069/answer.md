```python
# At end-of-bullet positions in loop regions (actual token '\n'), logprob of the '\n\n' alternative (section end), orig vs edited
NN=tok.encode('\n\n').ids; N1=tok.encode('\n').ids; print(NN,N1)
nn_id=NN[0]
def alt_lp(tk,tp,i,p,tid):
    m=np.where(tk[i,p]==tid)[0]
    return float(tp[i,p][m[0]]) if len(m) else None
for i in range(6):
    t=ids[i]; d=meta['loop'][i]
    rows=[]
    for p in range(d['pl']+1,d['end']):
        if t[p]==N1[0]:
            rows.append((p, p>=d['start'], alt_lp(tk3,tp3,i,p-1,nn_id), alt_lp(tk4,tp4,i,p-1,nn_id)))
    pre=[r for r in rows if not r[1]]; lo=[r for r in rows if r[1]]
    f=lambda rs,k: np.mean([r[k] for r in rs if r[k] is not None]) if any(r[k] is not None for r in rs) else None
    print(d['pid'], 'pre n',len(pre),'nn-lp orig',f(pre,2),'edit',f(pre,3),'| loop n',len(lo),'nn-lp orig',f(lo,2),'edit',f(lo,3))
```