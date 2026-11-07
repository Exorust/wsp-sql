```python
# Hypothesis: current edit uses a different direction than u; measure norm and cosine
for L,c in cols.items():
    n=f'model.language_model.layers.{L}.mlp.down_proj.weight'
    o=load_original(n); a=torch.from_numpy(np.load(f'{W}/edited/{n}.npy')); b=torch.from_numpy(np.load(f'{W}/best_1/{n}.npy'))
    da=(a-o)[:,c]; db=(b-o)[:,c]
    print(L, 'norm da',float(da.norm()),'cos(da,u)',float(da@u/da.norm()),'cos(da,db)',float(da@db/da.norm()/db.norm()), 'norm db', float(db.norm()))
# what else could be the direction? check against raw E[</think>] (no gN) 
v = E[think_id[0]]; v=v/v.norm()
print('cos(u,v)',float(u@v))
for L,c in cols.items():
    n=f'model.language_model.layers.{L}.mlp.down_proj.weight'
    da=(torch.from_numpy(np.load(f'{W}/edited/{n}.npy'))-load_original(n))[:,c]
    print(L,'cos(da,v)',float(da@v/da.norm()))
```