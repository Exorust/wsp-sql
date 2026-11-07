```python
# Decision B predicted effect: scale {L22n817, L23n879, L23n935} by k=2 (direct effect) on nl-vs-nlnl margins at line ends
def predB(k=2.0, neurons=((22,817),(23,879),(23,935))):
    out=[]
    for r in de.itertuples():
        delta=0
        for (L,n) in neurons:
            delta+=(k-1)*neuron_contrib(L,r.i,r.j-1,198,271)[n]
        out.append(r.margin+delta)
    return np.array(out)
nm=predB(2.0); nm3=predB(3.0)
kind=np.where(de.chosen=='nlnl','nlnl',np.where(de.margin<3,'nl_soft','nl_hard'))
for kd in ['nl_hard','nl_soft','nlnl']:
    m=kind==kd
    print(kd, 'n',m.sum(),'orig margin mean %.2f, flips(<0): %d'%(de.margin[m].mean(),(de.margin[m]<0).sum()), '| k=2: mean %.2f flips %d'%(nm[m].mean(),(nm[m]<0).sum()), '| k=3: mean %.2f flips %d'%(nm3[m].mean(),(nm3[m]<0).sum()))
# where are these neurons active? top tokens by |act|
for (L,n) in [(22,817),(23,879),(23,935)]:
    o,top=profile(L,n,{198,271})
    print(f'L{L}n{n}: at newline toks mean act %.2f | elsewhere mean %.2f mean|.| %.2f p99 %.2f'%(np.nanmean([o[i][0] for i in o]),np.mean([o[i][1] for i in o]),np.mean([o[i][2] for i in o]),np.mean([o[i][3] for i in o])),'top:',[(repr(t),v) for t,v in top[:6]])
```