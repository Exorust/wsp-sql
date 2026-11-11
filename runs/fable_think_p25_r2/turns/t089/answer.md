```python
# Decompose last layer (23) into attention and MLP contributions to the \n\n-\n logit at the decision positions; then per-neuron
Wd23=load('model.language_model.layers.23.mlp.down_proj.weight').numpy()  # [1024,3584]
A23=np.load(F+'/mlp_down_in_L23.npy')
proj=(d2@Wd23)  # per-neuron direction weight [3584]
def decomp(ps):
    att=[];mlp=[];neu=[]
    for (i,q) in ps:
        rms=np.sqrt((H[24][i,q].astype(np.float32)**2).mean()+1e-6)
        a=A23[i,q].astype(np.float32)
        contrib=a*proj/rms  # per-neuron
        m=contrib.sum(); tot=(H[24][i,q].astype(np.float32)-H[23][i,q].astype(np.float32))@d2/rms
        att.append(tot-m); mlp.append(m); neu.append(contrib)
    return np.array(att),np.array(mlp),np.array(neu)
R={k:decomp(v) for k,v in cls_pos.items()}
for k in R: print(k, 'attn %.2f mlp %.2f'%(R[k][0].mean(),R[k][1].mean()))
```