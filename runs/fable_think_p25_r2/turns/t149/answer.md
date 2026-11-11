```python
# Determine whether hidden_L24 is pre- or post-final-norm: compare logit diffs computed both ways against actual topk logprobs
def logit_diffs(x, prenorm):
    if prenorm: xn=x/np.sqrt((x**2).mean()+1e-6)*(1+Wn.numpy())
    else: xn=x
    lg=E.numpy()@xn; return lg
errs={True:[],False:[]}
for i in range(4):
    ids=ids5[i]
    for p in range(150, len(ids)-1, 37):
        x=np.asarray(H[24][i,p]).astype(np.float32)
        ids_k=tk5[i,p]; lp_k=tl5[i,p]
        for pre in [True,False]:
            lg=logit_diffs(x,pre)
            pred=lg[ids_k]-lg[ids_k[0]]; act=lp_k-lp_k[0]
            errs[pre].append(np.abs(pred-act).mean())
print('mean abs err prenorm-assumption %.3f, postnorm-assumption %.3f'%(np.mean(errs[True]), np.mean(errs[False])))
print('RMS by layer at pos 200 text0:', [round(float(np.sqrt((np.asarray(H[l][0,200]).astype(np.float32)**2).mean())),2) for l in range(25)])
```