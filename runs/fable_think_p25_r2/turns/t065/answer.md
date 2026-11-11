```python
# Branch-point analysis: within loop regions, at newline tokens, what is the next-token distribution? Does ablation raise P(escape tokens like '\n\n', '3.', '</think>')?
req3=json.load(open(W+'/tf3_req.json'))
texts=req3['texts']; print(len(texts), req3['return'])
tk3=np.load(W+'/fwd_3/topk_ids.npy'); tp3=np.load(W+'/fwd_3/topk_logprobs.npy')
tk4=np.load(W+'/fwd_4/topk_ids.npy'); tp4=np.load(W+'/fwd_4/topk_logprobs.npy')
print(tk3.shape)
ids=[tok.encode(t).ids for t in texts]
print([len(x) for x in ids[:6]], m3['lengths'][:6] if 'lengths' in m3 else None)
```