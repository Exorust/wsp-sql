```python
# Examine candidate repetition-detector neurons: activation at each rep position, distribution over ALL positions (prompt+answer), and per-text
cands=[(23,1576),(22,1494),(19,922),(17,1025),(18,226),(21,206),(20,1162),(23,1937)]
lensT=m13['lengths']
for L,n in cands:
    A=acts[L][:,:,n].astype(np.float32)
    allv=np.concatenate([A[k,:lensT[k]] for k in range(21)])
    repv=[float(A[k,p]) for k,p in rep_nl]; nonv=[float(A[k,p]) for k,p in non_nl]
    # where are the top activations overall?
    flat=[(float(A[k,p]),k,p) for k in range(21) for p in range(lensT[k])]
    flat.sort(reverse=True)
    print(f'L{L}n{n}: rep vals',np.round(repv,2),'| non max',round(max(nonv),2),'| all: p99.9',round(float(np.percentile(allv,99.9)),2),'max',round(float(allv.max()),2),
          '| top5 positions:',[(round(v,2),k,p,repr(tok.decode(enc13[k][max(0,p-3):p+1]))[-28:]) for v,k,p in flat[:5]])
```