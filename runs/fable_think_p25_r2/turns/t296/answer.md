```python
# Survey gen_16 classes/errors; verify L16 neuron 3 is a near-constant-sign neuron (fwd_12 mlp acts)
print(Counter(r['cls'] for r in rows))
print(os.listdir(os.path.join(W,'fwd_12'))[:20])
try:
    m16=np.load(os.path.join(W,'fwd_12','mlp_act_L16.npy'), mmap_mode='r')
    a=np.asarray(m16[:,:,3]).astype(np.float32); lp12=np.load(os.path.join(W,'fwd_12','token_logprobs.npy'))
    mask=~np.isnan(lp12)
    print('neuron3 L16: mean',a[mask].mean(),'std',a[mask].std(),'min',a[mask].min(),'max',a[mask].max(), 'frac<0', (a[mask]<0).mean())
except Exception as e: print(e)
errs=[r for r in rows if r['cls']=='no_such_column']
for r in errs[:12]:
    print('--',r['id'],r['db'],'|',r['err'][:80],'|',r['sql'][:160].replace('\n',' '))
```