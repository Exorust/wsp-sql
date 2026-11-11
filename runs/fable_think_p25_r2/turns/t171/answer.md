```python
# fwd_10 (edited): did </think> become the top prediction after '<think>\n'? SQL logprobs vs original (fwd_9 T2 for first 4)
d10=os.path.join(W,'fwd_10'); lp10=np.load(os.path.join(d10,'token_logprobs.npy')); tk10=np.load(os.path.join(d10,'topk_ids.npy')); tl10=np.load(os.path.join(d10,'topk_logprobs.npy'))
ids10=[tok.encode(t).ids for t in texts10]
orig_T2={kinds9[i][1]:i for i in [1,3,5,7]}
for i,(kind,pid) in enumerate(kinds10):
    ids=ids10[i]; pos=ids.index(248068); pth=ids.index(TH)
    pf=[p for p in range(pth,len(ids)) if ids[p]==71093]; body=list(range(pf[0]+3,pf[1]))
    top=[(tok.decode([int(a)])[:8], round(float(b),2)) for a,b in zip(tk10[i,pos+1][:3], tl10[i,pos+1][:3])]
    o=''
    if pid in orig_T2:
        j=orig_T2[pid]; idsj=ids9[j]; pthj=idsj.index(TH); pfj=[p for p in range(pthj,len(idsj)) if idsj[p]==71093]; bodyj=list(range(pfj[0]+3,pfj[1]))
        o=' | orig SQL mean %.3f'%np.mean(lp9[j,bodyj])
    print(pid, 'len',len(ids), '</think> lp %.2f'%lp10[i,pth], 'top after <think>\\n:', top, '| after: %s'%[round(float(lp10[i,p]),2) for p in range(pth+1,pth+5)], '| SQL mean %.3f'%np.mean(lp10[i,body]), o)
```