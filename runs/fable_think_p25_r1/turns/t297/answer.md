```python
# Hypothesis: fwd_14 contains attention for the sakila 'film.id' case; inspect files and the logprob/topk at 'id' position
print(os.listdir(f'{W}/fwd_14'))
m14=json.load(open(f'{W}/fwd_14/meta.json')); print({k:(v if k!='files' else len(v)) for k,v in m14.items()})
T14=json.load(open(f'{W}/req14.json'))['texts']
lp=np.load(f'{W}/fwd_14/token_logprobs.npy'); tk=np.load(f'{W}/fwd_14/topk_ids.npy'); tkl=np.load(f'{W}/fwd_14/topk_logprobs.npy')
print(lp.shape, tk.shape)
ids=tok.encode(T14[1]).ids; print(len(ids))
# find the answer region: locate 'film.id' tokens
s=tok.decode(ids[-60:]); print(repr(s))
st=len(ids)-60
for p in range(st,len(ids)):
    print(p, repr(tok.decode([ids[p]])), round(float(lp[1,p]),2), [ (tok.decode([int(t)]), round(float(l),1)) for t,l in zip(tk[1,p,:4], tkl[1,p,:4])])
```