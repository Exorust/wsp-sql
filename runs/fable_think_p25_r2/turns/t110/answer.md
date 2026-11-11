```python
# Reconstruct layer-23 per-head outputs from recorded attention patterns + recorded layer inputs; validate against residual difference
F6=f'{W}/fwd_6'
H23_6=np.load(f'{F6}/hidden_L23.npy'); H24_6=np.load(f'{F6}/hidden_L24.npy'); M23_6=np.load(f'{F6}/mlp_down_in_L23.npy')
A23=[np.load(f'{F6}/attn_L23_text{i}.npy') for i in range(2)]
print(A23[0].shape, A23[0].dtype)
L='model.language_model.layers.23.'
Wq=load_original(L+'self_attn.q_proj.weight').numpy(); Wk=load_original(L+'self_attn.k_proj.weight').numpy(); Wv=load_original(L+'self_attn.v_proj.weight').numpy()
Wo=load_original(L+'self_attn.o_proj.weight').numpy(); win=load_original(L+'input_layernorm.weight').numpy()
print('input_layernorm w stats', win.mean().round(3), win.std().round(3), '| q_norm', load_original(L+'self_attn.q_norm.weight').numpy().mean().round(3))
def rms(x): return x/np.sqrt((x**2).mean(-1,keepdims=True)+1e-6)
lens6=[424,621]
def head_outputs(n):
    T=lens6[n]; x=rms(H23_6[n,:T].astype(np.float32))*(1+win)      # [T,1024] attention input
    V=(x@Wv.T).reshape(T,2,256)                                      # [T,kv,256]
    G=(x@Wq.T).reshape(T,8,512)[:,:,256:]                            # gate per head [T,8,256]
    outs=np.zeros((8,T,1024),np.float32)
    for h in range(8):
        att=A23[n][h,:T,:T].astype(np.float32)@V[:,h//4]             # [T,256]
        att=att/(1+np.exp(-G[:,h]))
        outs[h]=att@Wo[:,h*256:(h+1)*256].T
    return outs
HO=[head_outputs(n) for n in range(2)]
for n in range(2):
    T=lens6[n]; true=H24_6[n,:T].astype(np.float32)-H23_6[n,:T].astype(np.float32)-M23_6[n,:T].astype(np.float32)@Wd23.T
    rec=HO[n].sum(0); err=np.linalg.norm(rec-true,axis=1)/np.linalg.norm(true,axis=1)
    print(n,'rel err median/max', np.median(err).round(3), err.max().round(3))
```