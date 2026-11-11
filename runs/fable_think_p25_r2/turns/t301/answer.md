```python
# Re-run SQL-region logprob comparison, building the fence string without literal triple backticks
FENCE='`'*3+'sql\n'
def sql_mean(lp, texts):
    out=[]
    for i,t in enumerate(texts):
        pre=t.index(FENCE)+len(FENCE)
        npre=len(tok.encode(t[:pre]).ids)
        L=int(np.sum(~np.isnan(lp[i])))+1
        out.append(float(np.nanmean(lp[i,npre:L])))
    return np.array(out)
s13=sql_mean(lp13,texts); s14=sql_mean(lp14,texts); s15=sql_mean(lp15,texts)
print('13',s13.mean().round(4),'14',s14.mean().round(4),'15',s15.mean().round(4))
d=s14-s13; print('14-13',d.mean().round(4),'se',(d.std()/np.sqrt(32)).round(4))
d=s15-s13; print('15-13',d.mean().round(4),'se',(d.std()/np.sqrt(32)).round(4))
print([f for f in os.listdir(os.path.join(W,'fwd_12')) if 'mlp' in f])
```