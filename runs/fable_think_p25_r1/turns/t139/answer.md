```python
# Activation profiles of candidate neurons: where are they active? (specificity to '\n\n' positions / line ends)
def profile(L,n,ctx_ids):
    a=M[L][:,:,n].astype(np.float32)  # [6,1600]
    out={}
    for i in range(6):
        ids=enc[i]; T=len(ids)
        act=a[i,:T]
        mask=np.array([x in ctx_ids for x in ids])
        out[i]=(act[mask].mean() if mask.any() else np.nan, act[~mask].mean(), np.abs(act[~mask]).mean(), np.percentile(np.abs(act[~mask]),99))
    allact=np.concatenate([a[i,:len(enc[i])] for i in range(6)]); allids=np.concatenate([enc[i] for i in range(6)])
    top=np.argsort(-np.abs(allact))[:8]
    return out, [(tok.decode([int(allids[t])]), round(float(allact[t]),2)) for t in top]
for (L,n) in [(23,932),(23,385),(22,1267),(22,223),(22,87),(18,128),(20,669),(23,580),(22,796)]:
    o,top=profile(L,n,{271})
    print(f'L{L}n{n}: at \\n\\n mean act %.2f | elsewhere mean %.2f, mean|.| %.2f, p99|.| %.2f'%(np.nanmean([o[i][0] for i in o]),np.mean([o[i][1] for i in o]),np.mean([o[i][2] for i in o]),np.mean([o[i][3] for i in o])), '| top |act| tokens:',[(repr(t),v) for t,v in top[:6]])
```