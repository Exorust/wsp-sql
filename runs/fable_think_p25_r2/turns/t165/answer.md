```python
# Delta between T1 and T2 states at the boundary position, per layer: norm, consistency across pairs, vs residual RMS
pairs=[(0,1),(2,3),(4,5),(6,7)]
for L in [10,12,14,16,17,18,19,20,21,22,23]:
    ds=[]; rms=[]
    for a,b in pairs:
        pa=ids9[a].index(248068)+1; pb=ids9[b].index(248068)+1
        xa=np.asarray(H9[L+1][a,pa]).astype(np.float32); xb=np.asarray(H9[L+1][b,pb]).astype(np.float32)
        ds.append(xa-xb); rms.append(np.sqrt((xb**2).mean()))
    ds=np.stack(ds); m=ds.mean(0)
    cos=[float(d@m/np.linalg.norm(d)/np.linalg.norm(m)) for d in ds]
    # consistency of T2 state across prompts (incl. T3/T4 boundary): cosine of x_b with mean
    xb_all=np.stack([np.asarray(H9[L+1][i,ids9[i].index(248068)+1]).astype(np.float32) for i in [1,3,5,7,8,9,10]])
    xbm=xb_all.mean(0); cosb=[float(x@xbm/np.linalg.norm(x)/np.linalg.norm(xbm)) for x in xb_all]
    print(f'after L{L}: |Delta| {np.linalg.norm(m):.3f}  resid RMS*32 {np.mean(rms)*32:.3f}  pair-cos {np.round(cos,2)}  T2-state cos across prompts min {min(cosb):.3f}')
```