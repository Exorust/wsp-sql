```python
# Hypothesis: build the 'Okay'-steer variant (same neurons/alphas, direction u_okay) and save it as the current edit; keep v2 in best_1.
print(os.listdir(W+'/best_1'))
for L,(n,a) in alphas.items():
    name='model.language_model.layers.%d.mlp.down_proj.weight'%L
    W0=load_original(name).clone(); W0[:,n]+=a*u_okay; save_edit(name,W0)
print(edited())
# choose 48 problems from gen12 (known v2 outcomes), random but fixed seed
rng=np.random.RandomState(7); ids12=[r['id'] for r in rows]; sub48=sorted(rng.choice(ids12,48,replace=False).tolist())
v2acc=np.mean([ (r['cls']=='correct') for r in rows if r['id'] in sub48]); print('v2 acc on sub48',v2acc)
json.dump(sub48,open(W+'/sub48.json','w')); print(json.dumps(sub48))
```