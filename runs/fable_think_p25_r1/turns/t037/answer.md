```python
# Induction scores for all full-attention heads: attention to (position after most recent previous occurrence of current token)
LAY=[3,7,11,15,19,23]
def induction_score(A, ids, qrange):
    T=len(ids); last={}; prev_next=np.full(T,-1)
    for j in range(T):
        if ids[j] in last: prev_next[j]=last[ids[j]]+1
        last[ids[j]]=j
    sc=np.zeros(A.shape[0]); n=0
    for q in qrange:
        if prev_next[q]>=0 and prev_next[q]<=q:
            sc+=A[:,q,prev_next[q]]; n+=1
    return sc/max(n,1)
for L in LAY:
    for ti,ids in enumerate([ids0,ids1]):
        A=np.load(f"{F2}/attn_L{L}_text{ti}.npy")
        T=len(ids); onset = 740 if ti==0 else 1090
        pre=induction_score(A, ids, range(250 if ti==0 else 570, onset))
        loop=induction_score(A, ids, range(onset, T))
        print(f"L{L} text{ti} pre-loop:", np.round(pre,2), " loop:", np.round(loop,2))
```