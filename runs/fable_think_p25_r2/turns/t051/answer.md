```python
# Hypothesis: ablating L15h7, L11h1, L23h5 lowers loop rep1/rep2 logprob more than pre-loop and gold SQL
e1=analyze(W+'/fwd_4', verbose=False)
for k in base:
    if k.startswith('_'): print(k, 'base',base[k],'\n     edit',e1[k])
    else: print(f'{k:12s} base {base[k]:.4f} edit {e1[k]:.4f} diff {e1[k]-base[k]:+.4f}')
# where in loop does the edited model deviate? show top-1 differences in rep2 for text 0..5
lp4=np.load(W+'/fwd_4/token_logprobs.npy'); tk4=np.load(W+'/fwd_4/topk_ids.npy'); tkl4=np.load(W+'/fwd_4/topk_logprobs.npy')
for i,d in enumerate(meta['loop']):
    ids=tok.encode(loop_texts[i]).ids; T=len(ids); st,P=d['start'],d['P']
    dev=[(t,tok.decode([ids[t]]),tok.decode([int(tk4[i,t-1,0])]),round(float(lp4[i,t]),2)) for t in range(st+P,T) if tk4[i,t-1,0]!=ids[t]]
    print(d['pid'],'n_dev',len(dev),dev[:4])
```