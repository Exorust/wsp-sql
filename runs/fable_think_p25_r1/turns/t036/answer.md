```python
# Attention patterns of layer-23 heads at decision positions: mass on previous NL tokens (induction targets), on previous '`.' tokens, on schema region
A23=[np.load(f"{F2}/attn_L23_text{ti}.npy") for ti in range(2)]
print(A23[0].shape)
def head_mass(ti, A, t, ids):
    q=t-1  # query position = the token before the decision token
    nl_pos=[j for j in range(q) if ids[j]==NL]
    nl2_pos=[j for j in range(q) if ids[j]==NL2]
    dot_pos=[j for j in range(q) if ids[j]==ids[q]]  # previous '`.' tokens
    out=[]
    for h in range(A.shape[0]):
        a=A[h,q,:q+1]
        out.append((a[nl_pos].sum(), a[nl2_pos].sum(), a[dot_pos].sum(), a[q], a[:245].sum()))
    return np.array(out)
for ti,(A,ids,dd) in enumerate([(A23[0],ids0,dec),(A23[1],ids1,dec1)]):
    print("text",ti)
    for t in dd[::4]:
        m=head_mass(ti,A,t,ids)
        print(t, "NL-mass per head:", np.round(m[:,0],2), " NL2:", np.round(m[:,1],2), " self:", np.round(m[:,3],2), " prompt:", np.round(m[:,4],2))
```