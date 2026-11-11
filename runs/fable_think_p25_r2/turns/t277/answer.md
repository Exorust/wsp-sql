```python
# Build steering edit: L16 MLP neuron 3 (near-constant act ~0.37) carries alpha * mean INSTR1-shift direction at hidden_L16
v16=np.array(diffs[16]).mean(0).astype(np.float32); print('v16 norm',np.linalg.norm(v16))
A16=np.load(d12+'mlp_down_in_L16.npy'); a3=np.concatenate([A16[j,1:n].astype(np.float32)[:,3] for j,(a,b,n) in enumerate(spans)])
print('neuron3 act over all tokens: mean %.3f sd %.3f min %.3f max %.3f'%(a3.mean(),a3.std(),a3.min(),a3.max()))
abar=float(a3.mean())
name16='model.language_model.layers.16.mlp.down_proj.weight'
W16o=load_original(name16); print(W16o.shape, 'col3 norm', float(W16o[:,3].norm()), 'typical col norm', float(W16o.norm(dim=0).median()))
import torch
def make_steer(alpha):
    Wn=W16o.clone(); Wn[:,3]+= torch.from_numpy(v16)*(alpha/abar); return Wn
alpha=3.0; Wn=make_steer(alpha); save_edit(name16,Wn); np.save(W+'/v16.npy',v16)
print(edited(), 'added col norm', float((Wn[:,3]-W16o[:,3]).norm()), 'expected shift norm', alpha*np.linalg.norm(v16))
```