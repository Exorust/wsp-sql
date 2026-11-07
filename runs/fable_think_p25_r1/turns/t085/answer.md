```python
# Analyze fwd_4 (original) vs fwd_5 (edited: 4 induction heads zeroed): effect on loop decision points and on gold SQL logprobs
items = json.load(open(f"{W}/req4_items.json"))
print(items.keys(), len(items['loop']), len(items.get('gold',[])))
lp4 = np.load(f"{W}/fwd_4/token_logprobs.npy"); lp5 = np.load(f"{W}/fwd_5/token_logprobs.npy")
ti4 = np.load(f"{W}/fwd_4/topk_ids.npy"); tl4 = np.load(f"{W}/fwd_4/topk_logprobs.npy")
ti5 = np.load(f"{W}/fwd_5/topk_ids.npy"); tl5 = np.load(f"{W}/fwd_5/topk_logprobs.npy")
print(lp4.shape, ti4.shape)
# loop region: tokens from onset to end; compare mean logprob of actual tokens (copied continuation) in loop region
loops = items['loop']
for i,it in enumerate(loops):
    ids = tok.encode(it['text']).ids
    T = len(ids); on=it['onset']
    a=np.nanmean(lp4[i,on:T]); b=np.nanmean(lp5[i,on:T])
    pre_a=np.nanmean(lp4[i,on-200:on]); pre_b=np.nanmean(lp5[i,on-200:on])
    print(it['id'], T, on, it['period'], f"loop lp orig {a:.3f} edited {b:.3f} | pre-loop orig {pre_a:.3f} edited {pre_b:.3f}")
```