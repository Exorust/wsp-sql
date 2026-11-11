```python
# Scan layers 14-20 for near-constant neurons over SQL tokens (and check prompt-region behaviour)
cands=[]
for l in [14,16,17,18,19,20]:
    A=np.load(d12+f'mlp_down_in_L{l}.npy')
    sqlA=np.concatenate([A[j,a:b].astype(np.float32) for j,(a,b,n) in enumerate(spans)])
    prA=np.concatenate([A[j,5:a-8].astype(np.float32) for j,(a,b,n) in enumerate(spans)])
    mu=sqlA.mean(0); sd=sqlA.std(0); frac_sign=(np.sign(sqlA)==np.sign(mu)).mean(0)
    score=np.abs(mu)/(sd+1e-3)
    idx=np.argsort(-score)[:6]
    for i in idx:
        cands.append((l,int(i),round(float(mu[i]),3),round(float(sd[i]),3),round(float(frac_sign[i]),2),round(float(prA[:,i].mean()),3),round(float(prA[:,i].std()),3)))
    del A
for c in cands: print(c)
```