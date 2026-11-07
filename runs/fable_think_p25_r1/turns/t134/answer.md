```python
# Per-neuron direct logit attribution (indent minus digit) for MLPs L16-23 at the '\n\n' decision points
Wd={L:load_original(f'model.language_model.layers.{L}.mlp.down_proj.weight') for L in range(16,24)}
M={L:np.load(F+f'mlp_down_in_L{L}.npy') for L in range(16,24)}
def rms_of(i,j):
    h=h23[i,j].astype(np.float32); return float(np.sqrt((h*h).mean()+eps))
def neuron_contrib(L,i,j,tid_a,tid_b):
    d=((E[tid_a]-E[tid_b])*nw)            # [1024]
    w=(d@Wd[L]).numpy()                   # [3584] per-neuron direction weight
    a=M[L][i,j].astype(np.float32)
    return a*w/rms_of(i,j)                # approximate (rms of final resid not exactly known; use layer23 input rms)
pts=[(2,811,id_3),(2,1071,id_4),(1,1067,id_3),(3,470,id_3)]
for L in range(16,24):
    tot=[]
    C=np.stack([neuron_contrib(L,i,j,id_ind,alt) for (i,j,alt) in pts])  # [4,3584]
    mean=C.mean(0)
    top_pos=np.argsort(-mean)[:5]; top_neg=np.argsort(mean)[:5]
    print(f'L{L} total per pt (ind-digit):', np.round(C.sum(1),2), '| toward indent:', [(int(n),round(float(mean[n]),2)) for n in top_pos], '| toward digit:', [(int(n),round(float(mean[n]),2)) for n in top_neg])
```