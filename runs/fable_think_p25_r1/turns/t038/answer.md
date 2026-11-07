```python
# Broader induction mass: attention to all positions p with ids[p-1]==ids[q] (tokens following any previous occurrence of current token)
def induction_mass(A, ids, qrange):
    T=len(ids); ids=np.array(ids)
    sc=np.zeros(A.shape[0]); n=0
    for q in qrange:
        p=np.where(ids[:q-1]==ids[q])[0]+1   # followers of previous occurrences, all < q
        if len(p)==0: continue
        sc+=A[:,q,p].sum(1); n+=1
    return sc/max(n,1)
res={}
for L in LAY:
    for ti,ids in enumerate([ids0,ids1]):
        A=np.load(f"{F2}/attn_L{L}_text{ti}.npy")
        T=len(ids); onset = 740 if ti==0 else 1090
        pre=induction_mass(A, ids, range(250 if ti==0 else 570, onset))
        loop=induction_mass(A, ids, range(onset, T))
        res[(L,ti)]=(pre,loop)
        print(f"L{L} text{ti} pre:", np.round(pre,2), " loop:", np.round(loop,2))
```