```python
# Characterize the current layer-18 down_proj edit: diff vs original, rank structure, relation to D18
name='model.language_model.layers.18.mlp.down_proj.weight'
Wd=load(name); Wo=load_original(name)
Dm=(Wd-Wo); print(Wd.shape, 'max|diff|',Dm.abs().max().item(), 'frob diff',Dm.norm().item(),'frob orig',Wo.norm().item())
nz_rows=(Dm.abs().sum(1)>0).sum().item(); nz_cols=(Dm.abs().sum(0)>0).sum().item(); print('nz rows',nz_rows,'nz cols',nz_cols)
U,S,Vh=torch.linalg.svd(Dm,full_matrices=False); print('top sv',S[:5].numpy())
d=torch.tensor(D); print('cos(U0,D18)',(U[:,0]@d/(U[:,0].norm()*d.norm())).item())
cols=torch.nonzero(Dm.abs().sum(0)>0).flatten(); print('cols edited',cols.tolist()[:40])
print('col deltas norm', Dm[:,cols].norm(dim=0).numpy()[:20], 'orig col norms', Wo[:,cols].norm(dim=0).numpy()[:20])
```