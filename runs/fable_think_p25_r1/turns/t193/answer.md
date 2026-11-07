```python
# Analyze fwd_10: lp of </think> at first position under the edit, and what it competes with; plus gold SQL token lps
lp10 = np.load(f"{W}/fwd_10/token_logprobs.npy"); tk10 = np.load(f"{W}/fwd_10/topk_ids.npy"); tkl10 = np.load(f"{W}/fwd_10/topk_logprobs.npy")
for n,t in enumerate(texts10):
    ids = tok.encode(t).ids
    q = ids.index(248068)+1      # '\n' after <think>
    assert ids[q+1]==ID_TC
    print(n, "lp(</think>) =", round(float(lp10[n,q+1]),2), " top:", [(tok.decode([int(i)]), round(float(l),2)) for i,l in zip(tk10[n,q], tkl10[n,q])][:4])
    # after </think>: next '\n\n'
    print("   after </think>:", [(tok.decode([int(i)]), round(float(l),2)) for i,l in zip(tk10[n,q+1], tkl10[n,q+1])][:3],
          "| gold sql mean lp:", round(float(np.nanmean(lp10[n, q+5:len(ids)-3])),3), "min:", round(float(np.nanmin(lp10[n, q+5:len(ids)-3])),2))
```