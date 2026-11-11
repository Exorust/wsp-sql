```python
# Fix: total uses E diff on post-norm y; layer contributions use (1+w)*(E diff) on residual deltas
def layer_dla(Hs, i, pos, a, b, g=1.05):
    xs=np.stack([np.asarray(Hs[l][i,pos]).astype(np.float32) for l in range(24)])
    y=np.asarray(Hs[24][i,pos]).astype(np.float32)
    upost=(E[a]-E[b]).numpy(); upre=upost*(1+Wn.numpy())
    total=float(y@upost); s=np.sqrt((xs[23]**2).mean())*g
    c=np.zeros(25); c[0]=xs[0]@upre/s; c[1:24]=np.diff(xs,axis=0)@upre/s; c[24]=total-c[:24].sum()
    return c, total
C=np.stack([layer_dla(H,i,[p for p,x in enumerate(ids5[i]) if x==248068][0]+1,TH,THINKING)[0] for i in range(12)])
print(np.round(C.mean(0),2), 'total', round(C.sum(1).mean(),2))
```