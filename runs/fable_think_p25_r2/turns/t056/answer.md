```python
# Compare fwd_3 (original) vs fwd_4 (3 induction heads ablated): token logprobs in loop regions (pre-loop vs loop) and on gold SQL answers
meta=json.load(open(W+'/tf_set_meta.json'))
lp3=np.load(W+'/fwd_3/token_logprobs.npy'); lp4=np.load(W+'/fwd_4/token_logprobs.npy')
print(lp3.shape, lp4.shape)
m3=json.load(open(W+'/fwd_3/meta.json')); print({k:(v if not isinstance(v,list) else len(v)) for k,v in m3.items()})
for i,d in enumerate(meta['loop']):
    pl,st,en=d['pl'],d['start'],d['end']
    pre3=np.nanmean(lp3[i,pl:st]); pre4=np.nanmean(lp4[i,pl:st])
    lo3=np.nanmean(lp3[i,st:en]); lo4=np.nanmean(lp4[i,st:en])
    print(f"{d['pid']}: pre-loop orig {pre3:.3f} edit {pre4:.3f} | loop orig {lo3:.3f} edit {lo4:.3f} (P={d['P']})")
# gold texts: last part is the assistant answer; need the prompt lengths -- check tf3_req to find boundaries
req=json.load(open(W+'/tf3_req.json'))
print(req.keys() if isinstance(req,dict) else type(req))
```