```python
# Per-layer direct logit attribution of (\n\n - \n) at decision positions: pre-loop continuation, loop continuation, section ends
def positions(i):
    t=ids5[i]; pl=tf5_meta[i]['pl']; st=tf5_meta[i]['start']
    pre=[q for q in range(pl, L5[i]-1) if t[q+1]==198 and q<st]
    loo=[q for q in range(pl, L5[i]-1) if t[q+1]==198 and q>=st]
    sec=[q for q in range(pl, L5[i]-1) if t[q+1]==271]
    return pre,loo,sec
cls_pos={'pre':[], 'loop':[], 'sec':[]}
for i in range(12):
    pre,loo,sec=positions(i)
    cls_pos['pre']+=[(i,q) for q in pre]; cls_pos['loop']+=[(i,q) for q in loo]; cls_pos['sec']+=[(i,q) for q in sec]
print({k:len(v) for k,v in cls_pos.items()})
def layer_dla(ps):
    out=np.zeros((len(ps),25))
    for n,(i,q) in enumerate(ps):
        rms=np.sqrt((H[24][i,q].astype(np.float32)**2).mean()+1e-6)
        prev=H[0][i,q].astype(np.float32)
        out[n,0]=prev@d2/rms
        for l in range(1,25):
            cur=H[l][i,q].astype(np.float32); out[n,l]=(cur-prev)@d2/rms; prev=cur
    return out
D={k:layer_dla(v) for k,v in cls_pos.items()}
print('layer: pre | loop | sec   (mean contribution to logit(nn)-logit(n))')
for l in range(25):
    print(f'{l:2d}: {D["pre"][:,l].mean():6.2f} {D["loop"][:,l].mean():6.2f} {D["sec"][:,l].mean():6.2f}')
print('total', D['pre'].sum(1).mean(), D['loop'].sum(1).mean(), D['sec'].sum(1).mean())
```