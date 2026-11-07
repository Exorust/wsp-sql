```python
# Hypothesis: probe B (zeroing 4 induction heads) barely changed copied-token lp at loop points -> copying is implemented elsewhere (DeltaNet); compare fwd_4 vs fwd_5 token logprobs.
m4=json.load(open(W+'/fwd_4/meta.json')); m5=json.load(open(W+'/fwd_5/meta.json'))
t4=np.load(W+'/fwd_4/token_logprobs.npy'); t5=np.load(W+'/fwd_5/token_logprobs.npy'); print(t4.shape,t5.shape, m4['lengths'][:5], m5['lengths'][:5])
req4=json.load(open(W+'/req4.json')); tx4=req4['texts']; print(len(tx4))
setA=json.load(open(W+'/setA.json')); print(type(setA), len(setA), list(setA[0].keys()) if isinstance(setA,list) else '')
```