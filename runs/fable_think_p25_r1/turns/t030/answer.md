```python
# Align tokens (variant A) with logprobs; check how predictable the loop region is
lp=np.load(f"{F2}/token_logprobs.npy"); tk=np.load(f"{F2}/topk_ids.npy"); tlp=np.load(f"{F2}/topk_logprobs.npy")
print(lp.shape, tk.shape)
toks=[tok.encode(render(c[0]['content'],c[1]['content'],'A')).ids for c in chats_attn]
for ti in range(2):
    ids=np.array(toks[ti]); T=len(ids)
    # logprob at position t is for predicting token t (nan at 0)
    top1=tk[ti,:T,0]
    # positions: find where assistant content starts
    a_start = len(tok.encode(render(chats_attn[ti][0]['content'],'','A')).ids)-3  # approx
    print("text",ti,"T",T, "mean lp assistant part", np.nanmean(lp[ti,a_start:T]))
    # decode a slice near the end and show per-token lp
    for t in range(T-40, T):
        print(repr(tok.decode([ids[t]])), round(float(lp[ti,t]),2), 'top1', repr(tok.decode([top1[t-1]])) if t>0 else '', end=' | ')
    print()
```