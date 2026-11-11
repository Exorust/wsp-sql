```python
# fwd_9: per-text mean logprob over SQL tokens for T1 vs T2 pairs (4 problems)
F9=os.path.join(W,'fwd_9'); lp9=np.load(os.path.join(F9,'token_logprobs.npy')); tk9=np.load(os.path.join(F9,'topk_ids.npy'))
def sql_span(text):
    ids=tok.encode(text).ids; toks=[tok.decode([t]) for t in ids]
    s=text.rfind(FENCE+'sql\n'); pos=0; start=None
    for j,t in enumerate(toks):
        pos+=len(t)
        if start is None and pos>s+7: start=j
    return ids, start
for k in range(0,8,2):
    for i in (k,k+1):
        t=r9['texts'][i]; ids,st=sql_span(t); L=len(ids)
        seg=lp9[i,st+1:L]   # logprobs of SQL tokens (incl. closing fence)
        print(m9['kinds'][i], 'SQLtoks',L-st-1,'mean lp %.3f sum %.2f'%(seg.mean(), seg.sum()), ' first-SQL-token lp %.2f'%lp9[i,st+1])
```