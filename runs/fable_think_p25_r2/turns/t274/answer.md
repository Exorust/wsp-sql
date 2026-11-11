```python
# Scan layers 14-20 for neurons whose activation is near-constant (same sign, low CV) over SQL tokens and also over the prompt
T12=r12['texts']; spans=[my_sql_span(t) for t in T12]
cands=[]
for l in [14,16,17,18,19,20]:
    A=np.load(d12+f'mlp_act_L{l}.npy')  # [N,T,3584] float16
    sqlA=np.concatenate([A[j,a:b].astype(np.float32) for j,(a,b,n) in enumerate(spans)])  # SQL tokens
    prA=np.concatenate([A[j,5:a-8].astype(np.float32) for j,(a,b,n) in enumerate(spans)])  # prompt tokens
    mu=sqlA.mean(0); sd=sqlA.std(0); frac_sign=(np.sign(sqlA)==np.sign(mu)).mean(0)
    score=np.abs(mu)/(sd+1e-3)
    idx=np.argsort(-score)[:6]
    for i in idx:
        cands.append((l,int(i),round(float(mu[i]),3),round(float(sd[i]),3),round(float(frac_sign[i]),2),round(float(prA[:,i].mean()),3),round(float(prA[:,i].std()),3)))
    del A
for c in cands: print(c)
```