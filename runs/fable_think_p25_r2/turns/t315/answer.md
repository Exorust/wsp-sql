```python
# In-context INSTR1 effect on gold-SQL lp (fwd_13 texts 32-63 vs 0-31), and how INSTR1 was inserted (to build INSTR2/INSTR3 texts)
lp13full=np.load(os.path.join(W,'fwd_13','token_logprobs.npy'))
sb=sql_mean_full=None
def sql_mean2(lp, texts_, idxs):
    out=[]
    for j,i in enumerate(idxs):
        t=texts_[i]; pre=t.index(FENCE)+len(FENCE); npre=len(tok.encode(t[:pre]).ids); L=int(np.sum(~np.isnan(lp[i])))+1
        out.append(float(np.nanmean(lp[i,npre:L])))
    return np.array(out)
b=sql_mean2(lp13full,T,range(32)); a=sql_mean2(lp13full,T,range(32,64))
print('in-context INSTR1 gold lp gain',(a-b).mean().round(4),'se',((a-b).std()/np.sqrt(32)).round(4))
t0=T[0]; t32=T[32]; k=0
while t0[k]==t32[k]: k+=1
print('divergence at',k, repr(t0[k-60:k+40])); print(repr(t32[k-60:k+200]))
m643=np.asarray(m16[:,:,643]).astype(np.float32); print('neuron 643 L16 mean',m643[mask].mean().round(3),'std',m643[mask].std().round(3),'frac<0',(m643[mask]<0).mean().round(3))
```