```python
# Redo per-layer DLA correctly: hidden_L24 is post-norm; hidden_L23 is input to last layer. Estimate s=rms(final resid) ~ rms(hidden_L23)*g
def layer_dla(Hs, i, pos, u, g=1.05):
    xs=np.stack([np.asarray(Hs[l][i,pos]).astype(np.float32) for l in range(24)])  # L0..L23 residuals
    y=np.asarray(Hs[24][i,pos]).astype(np.float32)  # post-norm
    total=float(y@u)                      # exact logit diff
    s=np.sqrt((xs[23]**2).mean())*g      # estimated rms of final residual
    c=np.zeros(25); c[0]=xs[0]@u/s; c[1:24]=np.diff(xs,axis=0)@u/s; c[24]=total-c[:24].sum()
    return c, total
u=((E[TH]-E[THINKING])*(1+Wn)).numpy()
C=np.stack([layer_dla(H,i,[p for p,x in enumerate(ids5[i]) if x==248068][0]+1,u)[0] for i in range(12)])
print('per-layer DLA logit(</think>)-logit(Thinking) at <think>\\n pos (layers 0..23 as index 1..24; index0=embed):')
print(np.round(C.mean(0),2), 'total', round(C.sum(1).mean(),2))
```