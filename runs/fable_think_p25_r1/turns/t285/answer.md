```python
# Hypothesis: current edit = v2 with modified alphas; recover alphas for both edited and best_1 relative to original
E = load_original('model.language_model.embed_tokens.weight')
gN = load_original('model.language_model.norm.weight')
think_id = tok.encode('</think>').ids; print(think_id)
u = gN*E[think_id[0]]; u = u/u.norm()
cols={17:537,18:628,19:2424,20:1235}
for L,c in cols.items():
    n=f'model.language_model.layers.{L}.mlp.down_proj.weight'
    o=load_original(n); a=torch.from_numpy(np.load(f'{W}/edited/{n}.npy')); b=torch.from_numpy(np.load(f'{W}/best_1/{n}.npy'))
    da=(a-o); db=(b-o)
    print(L,c,'edited: alpha',float((da[:,c]@u)),'offcol',float(da.abs().sum()-da[:,c].abs().sum()),'| best_1 alpha',float(db[:,c]@u), 'orig col norm',float(o[:,c].norm()))
```