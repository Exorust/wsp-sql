```python
# Compare gold-SQL logprobs: fwd_13[:32] (pre-L16 baseline) vs fwd_14 / fwd_15 (two L16 strengths); and check L16 neuron-3 acts if available
lp13=np.load(os.path.join(W,'fwd_13','token_logprobs.npy'))[:32]
lp14=np.load(os.path.join(W,'fwd_14','token_logprobs.npy')); lp15=np.load(os.path.join(W,'fwd_15','token_logprobs.npy'))
req=json.load(open(os.path.join(W,'tf14_req.json')))
texts=req['texts']; print(req.get('model'), len(texts), list(req.keys()))
# locate SQL region: tokens after '<think>\n</think>\n\n```sql\n'
sql_lp={}
for name,lp in [('13',lp13),('14',lp14),('15',lp15)]:
    vals=[]; starts=[]
    for i,t in enumerate(texts):
        ids=tok.encode(t).ids
        pre=t.index('```sql\n')+len('```sql\n')
        npre=len(tok.encode(t[:pre]).ids)
        L=int(np.sum(~np.isnan(lp[i])))+1
        vals.append(np.nanmean(lp[i,npre:L]))
    sql_lp[name]=np.array(vals)
for k in ['13','14','15']: print(k, 'mean gold-SQL lp/token', sql_lp[k].mean().round(4))
print('14-13 per-text mean',(sql_lp['14']-sql_lp['13']).mean().round(4),'se',((sql_lp['14']-sql_lp['13']).std()/np.sqrt(32)).round(4))
print('15-13 per-text mean',(sql_lp['15']-sql_lp['13']).mean().round(4),'se',((sql_lp['15']-sql_lp['13']).std()/np.sqrt(32)).round(4))
print([f for f in os.listdir(os.path.join(W,'fwd_12')) if 'mlp' in f])
```