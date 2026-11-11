```python
# Check residual norms by layer and split layer 23 into attention vs MLP for the first-token decision
p=pos0[0]
print('norms:', [round(float(np.linalg.norm(H[l][0,p].astype(np.float32))),1) for l in range(25)])
Wd23=load('model.language_model.layers.23.mlp.down_proj.weight').numpy()
M23=np.load(f'{W}/fwd_5/mlp_down_in_L23.npy')
def split23(a,b,positions):
    d=((E[a]-E[b])*(1+wn)).numpy(); res=[]
    for n,pp in enumerate(positions):
        h24=H[24][n,pp].astype(np.float32); rms=np.sqrt((h24**2).mean()+1e-6)
        mlp=Wd23@M23[n,pp].astype(np.float32); tot=h24-H[23][n,pp].astype(np.float32); att=tot-mlp
        res.append([(att@d)/rms,(mlp@d)/rms,(H[23][n,pp].astype(np.float32)@d)/rms])
    return np.array(res)
r=split23(T_think,T_the,pos0); print('Thinking-The: attn, mlp, resid<=22 :', np.round(r.mean(0),2))
r=split23(T_end,T_think,pos0); print('</think>-Thinking: attn, mlp, resid<=22 :', np.round(r.mean(0),2))
print('mlp23 norm', round(float(np.linalg.norm(Wd23@M23[0,p].astype(np.float32))),1), 'h24-h23 norm', round(float(np.linalg.norm(H[24][0,p].astype(np.float32)-H[23][0,p].astype(np.float32))),1))
```