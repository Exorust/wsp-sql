```python
# Reload fwd_13 arrays
D=f'{W}/fwd_13'; m13=json.load(open(f'{D}/meta.json'))
lp13=np.load(f'{D}/token_logprobs.npy'); tk_ids=np.load(f'{D}/topk_ids.npy'); tk_lp=np.load(f'{D}/topk_logprobs.npy')
print(lp13.shape, tk_ids.shape)
enc13=[tok.encode(t).ids for t in texts13]
print([ (len(e),L) for e,L in zip(enc13[:4], m13['lengths'][:4])])
```