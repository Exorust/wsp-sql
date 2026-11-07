```python
# Fix: max-based selectivity for the candidate neurons (print compact numbers only)
def sel_stats(L,j):
    A=M[L]; at=np.array([A[i,pos_think[i],j] for i in range(6)],dtype=np.float32)
    mx=0; where=None
    for i in range(6):
        a=np.abs(A[i,:lens7[i],j].astype(np.float32)); a[pos_think[i]]=0
        k=int(a.argmax())
        if a[k]>mx: mx=float(a[k]); where=(i,k,repr(tok.decode(ids7[i][k-3:k+1])))
    return at.round(2).tolist(), round(mx,2), where
for (L,j) in [(18,628),(17,537),(17,2138),(17,1533),(18,2763),(19,2800),(20,2745),(20,1981)]:
    print(L,j, sel_stats(L,j))
print("rms h23 at pos:", np.sqrt((h23**2).mean(1)).round(2))
```