```python
# Split per-layer DLA into MLP (down_proj @ act) and attention remainder for layers 10..23, T1 vs T2
Wd={l:load(f'model.language_model.layers.{l}.mlp.down_proj.weight').numpy() for l in range(10,24)}
A9={l:np.load(os.path.join(d9,f'mlp_down_in_L{l}.npy'), mmap_mode='r') for l in range(10,24)}
upre=((E[TH]-E[THINKING])*(1+Wn)).numpy()
def split(i,pos,g=1.05):
    xs=np.stack([np.asarray(H9[l][i,pos]).astype(np.float32) for l in range(24)])
    y=np.asarray(H9[24][i,pos]).astype(np.float32); s=np.sqrt((xs[23]**2).mean())*g
    tot=float(y@(E[TH]-E[THINKING]).numpy())
    out={}
    for l in range(10,24):
        act=np.asarray(A9[l][i,pos]).astype(np.float32); mlp=Wd[l]@act
        mlp_c=float(mlp@upre/s)
        if l<23: layer_c=float((xs[l+1]-xs[l])@upre/s)
        else: layer_c=tot-float(xs[0]@upre/s)-float(np.diff(xs,axis=0)@upre/s).sum() if False else tot - float(xs[23]@upre/s)
        out[l]=(layer_c-mlp_c, mlp_c)
    return out
for kind,idx in [('T1',[0,2,4,6]),('T2',[1,3,5,7])]:
    acc=collections.defaultdict(lambda: np.zeros(2))
    for i in idx:
        pos=ids9[i].index(248068)+1
        for l,v in split(i,pos).items(): acc[l]+=np.array(v)/len(idx)
    print(kind, ' '.join(f'L{l}:a{acc[l][0]:+.1f}/m{acc[l][1]:+.1f}' for l in range(10,24)))
```