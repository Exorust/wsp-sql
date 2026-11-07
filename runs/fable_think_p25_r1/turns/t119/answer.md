```python
# Selectivity of candidate neurons using the max over other positions; look at layers 22-23 too; and residual norm at the position
def sel_stats(L,j):
    A=M[L]; at=np.array([A[i,pos_think[i]] for i in range(6)],dtype=np.float32)
    mx=0
    for i in range(6):
        a=np.abs(A[i,:lens7[i],j].astype(np.float32)); a[pos_think[i]]=0; mx=max(mx,a.max())
    return at.round(2).tolist(), float(mx)
for L in [23,22,21]:
    A=M[L]; at=np.stack([A[i,pos_think[i]].astype(np.float32) for i in range(6)])
    mx=np.zeros(3584,dtype=np.float32)
    for i in range(6):
        a=np.abs(A[i,:lens7[i]].astype(np.float32)); a[pos_think[i]]=0; mx=np.maximum(mx,a.max(0))
    sel=np.abs(at).min(0)/(mx+1e-3)
    for j in np.argsort(-sel)[:3]: print(L,int(j), round(float(sel[j]),2), at[:,j].round(2).tolist(), round(float(mx[j]),2))
for (L,j) in [(18,628),(17,537),(17,2138)]:
    print(L,j, sel_stats(L,j))
h23 = np.stack([H[23][i,pos_think[i]].astype(np.float32) for i in range(6)]); print("rms h23 at pos:", np.sqrt((h23**2).mean(1)).round(2))
h18 = np.stack([H[16][i,pos_think[i]].astype(np.float32) for i in range(6)]); print("rms h16 at pos:", np.sqrt((h18**2).mean(1)).round(2))
```