```python
# Hypothesis: fwd_13 holds TF logprobs for 7 answer-loop texts + 14 others; find loop decision points (where copied token wins) and margins.
F=W+'/fwd_13'; meta=json.load(open(F+'/meta.json')) if os.path.exists(F+'/meta.json') else None
print(meta if meta is None else {k:(v if not isinstance(v,list) or len(v)<30 else len(v)) for k,v in meta.items()})
tl=np.load(F+'/token_logprobs.npy'); tk=np.load(F+'/topk_ids.npy'); tkl=np.load(F+'/topk_logprobs.npy')
print(tl.shape,tk.shape)
texts13=r13['texts']; ids13=[tok.encode(t).ids for t in texts13]
print([len(x) for x in ids13][:8], r13['return'])
```