```python
# Find MLP neurons (layers 10-23) specific to the position right after <think> (both T1 '\n\n' and T2 '\n'), vs all other positions
bpos=[(i, ids9[i].index(248068)+1) for i in range(11)]  # position after <think> in every text
spec=[]
for l in range(10,24):
    A=np.asarray(A9[l]).astype(np.float32)  # [11,T,3584]
    T=A.shape[1]
    mask=np.zeros((11,T),bool)
    for i in range(11): mask[i,:len(ids9[i])]=True
    for i,p in bpos: mask[i,p]=False
    other=np.abs(np.where(mask[:,:,None],A,0)).max(axis=(0,1))  # max |act| elsewhere
    b1=np.stack([A[i,p] for i,p in bpos[:8:2]])  # T1 positions
    b2=np.stack([A[i,p] for i,p in bpos[1:8:2]+bpos[8:]])  # T2/T3/T4 positions ('\n' after <think>)
    for n in range(3584):
        m1=b1[:,n].mean(); m2=b2[:,n].mean()
        spec.append((l,n,m1,m2,other[n], min(np.abs(b2[:,n]).min(), np.abs(b1[:,n]).min())))
spec=np.array(spec)
# specificity: min |act| at boundary positions / max |act| elsewhere
ratio=spec[:,5]/(spec[:,4]+1e-6)
ordr=np.argsort(-ratio)[:25]
print('layer neuron meanT1 meanT2 maxElse minAbsBoundary ratio')
for k in ordr: print(int(spec[k,0]), int(spec[k,1]), *np.round(spec[k,2:6],3), round(float(ratio[k]),2))
```