```python
# Gold-SQL texts: compare logprob of answer tokens (after assistant start) orig vs edited; also greedy-argmax agreement with gold
golds = items['gold']
tot4=tot5=0; n=0; worse=0
for j,it in enumerate(golds):
    i = len(loops)+j
    ids = tok.encode(it['text']).ids; T=len(ids)
    # find answer start: position of last '<|im_start|>assistant'
    txt = it['text']; k = txt.rfind("assistant")
    pre = len(tok.encode(txt[:k]).ids)
    a=np.nansum(lp4[i,pre:T]); b=np.nansum(lp5[i,pre:T])
    acc4=(ti4[i,pre-1:T-1,0]==np.array(ids[pre:T])).mean(); acc5=(ti5[i,pre-1:T-1,0]==np.array(ids[pre:T])).mean()
    tot4+=a; tot5+=b; n+=T-pre
    print(it['id'], T-pre, f"sum lp orig {a:.1f} edited {b:.1f} argmax-acc {acc4:.2f}/{acc5:.2f}")
print("per-token mean", tot4/n, tot5/n)
```