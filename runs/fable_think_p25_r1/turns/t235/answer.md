```python
# Search L16-23 for neurons selective for 'the line just completed repeats an earlier line' at the '\n' position (decides AND/fence) and at line-end position (decides '\n' vs ';')
acts={L:np.load(f'{D}/mlp_down_in_L{L}.npy') for L in range(16,24)}
print(acts[23].shape, acts[23].dtype)
# positions
rep_nl=[];non_nl=[];rep_end=[];non_end=[]
for k,ids in enumerate(enc13):
    s=starts[k]; seen=set(); line_tokens=[]
    for p in range(s,len(ids)):
        if ids[p]==198:
            line=tok.decode(line_tokens).strip(); rep=line in seen; seen.add(line); line_tokens=[]
            if not line: continue
            (rep_nl if rep else non_nl).append((k,p)); (rep_end if rep else non_end).append((k,p-1))
        else: line_tokens.append(ids[p])
print(len(rep_nl),len(non_nl))
def gather(L,pos): return np.stack([acts[L][k,p].astype(np.float32) for k,p in pos])
for L in range(16,24):
    A_rep=gather(L,rep_nl); A_non=gather(L,non_nl)
    sd=acts[L][:,:].reshape(-1,3584).astype(np.float32).std(0)+1e-3
    score=(A_rep.mean(0)-A_non.mean(0))/sd
    # also require consistency: min over rep > max over non
    sel=(A_rep.min(0)-A_non.max(0))/sd
    top=np.argsort(-score)[:5]
    print(f'L{L} nl-pos top by mean diff:', [(int(n), round(float(score[n]),2), round(float(A_rep.mean(0)[n]),2), round(float(A_non.mean(0)[n]),2), round(float(A_non.max(0)[n]),2)) for n in top], '| best min-max sel', round(float(sel.max()),2), int(sel.argmax()))
```