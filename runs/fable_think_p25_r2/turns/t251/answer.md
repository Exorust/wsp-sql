```python
# Reconstruct exact MLP inputs at layer L for fwd_12 (h_L - down_proj @ act), normalise, and test SELECT-position separability
import torch
def mlp_inputs(L):
    hL=np.load(os.path.join(F12,f'hidden_L{L}.npy')).astype(np.float32)
    A=np.load(os.path.join(F12,f'mlp_down_in_L{L}.npy')).astype(np.float32)
    Wd=load(f'model.language_model.layers.{L}.mlp.down_proj.weight').numpy()   # [1024,3584]
    wpost=load(f'model.language_model.layers.{L}.post_attention_layernorm.weight').numpy()
    xpre=hL - A@Wd.T
    rms=np.sqrt((xpre**2).mean(-1,keepdims=True)+1e-6)
    xn=xpre/rms*(1+wpost)
    return xpre,xn,A
valid=np.zeros((36,330),bool)
for i in range(36): valid[i,1:lens12[i]]=True
isSEL=np.zeros((36,330),bool)
for i in range(36):
    for j in range(lens12[i]):
        if TOKS[i][j].strip()=='SELECT': isSEL[i,j]=True
print('n SELECT positions', isSEL.sum(), 'n valid', valid.sum())
for L in [14,16]:
    xpre,xn,A=mlp_inputs(L)
    Xs=xn[isSEL]; Xo=xn[valid&~isSEL]
    # fit on texts 0-23, test on 24-35
    tr=np.zeros((36,330),bool); tr[:24]=True
    mu_s=xn[isSEL&tr].mean(0); mu_o=xn[valid&~isSEL&tr].mean(0)
    g=mu_s-mu_o; g/=np.linalg.norm(g)
    ps=xn[isSEL&~tr]@g; po=xn[valid&~isSEL&~tr]@g
    print(f'L{L}: mean-diff gate: SELECT proj min {ps.min():.2f} mean {ps.mean():.2f} | other proj max {po.max():.2f} q99.9 {np.quantile(po,0.999):.2f} mean {po.mean():.2f} | rms of xn {np.sqrt((xn[valid]**2).mean()):.2f}')
    # which 'other' tokens come closest?
    idx=np.argsort(-po)[:5]; oth_tokens=[(S(TOKS[i][j]),round(float(xn[i,j]@g),2)) for (i,j) in zip(*np.where(valid&~isSEL&~tr)) ][0:0]
    coords=np.array(np.where(valid&~isSEL&~tr)).T[idx]; print('   closest others:', [(S(TOKS[i][j]), round(float(po[k]),2)) for k,(i,j) in zip(idx,coords)])
```