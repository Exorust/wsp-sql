```python
# fwd_9: check logprobs at the think boundary and SQL quality for T1/T2/T3/T4
d9=os.path.join(W,'fwd_9'); lp9=np.load(os.path.join(d9,'token_logprobs.npy')); tk9=np.load(os.path.join(d9,'topk_ids.npy')); tl9=np.load(os.path.join(d9,'topk_logprobs.npy'))
ids9=[tok.encode(t).ids for t in texts9b]
SQLF=tok.encode('sql').ids[0]
for i,(kind,pid) in enumerate(kinds9):
    ids=ids9[i]; pos=ids.index(248068); pth=ids.index(TH)
    # logprob of the token after <think>, of </think>, and mean logprob of SQL body (from 'SELECT' token after fence to final fence)
    pf=[p for p in range(pth,len(ids)) if ids[p]==71093]  # fences
    body=range(pf[0]+3, pf[1])  # after '```','sql','\n'
    print(kind,pid, 'tok after <think>:',repr(tok.decode([ids[pos+1]]))[:6], round(float(lp9[i,pos+1]),2), '| </think>:', round(float(lp9[i,pth]),2), '| after </think>:', [round(float(lp9[i,p]),2) for p in range(pth+1,pth+5)], '| SQL mean %.2f sum %.1f n %d'%(np.mean(lp9[i,list(body)]), np.sum(lp9[i,list(body)]), len(body)))
```