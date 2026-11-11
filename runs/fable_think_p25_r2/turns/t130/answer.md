```python
# Proper per-layer DLA at the first thinking token position for 2 texts (fwd_8), for Thinking-vs-The and Thinking-vs-Okay
H8={l:np.load(f'{F8}/hidden_L{l}.npy') for l in range(25)}
M8={l:np.load(f'{F8}/mlp_down_in_L{l}.npy') for l in range(18,24)}
A8=[np.load(f'{F8}/attn_L23_text{i}.npy') for i in range(2)]
def head_outputs8(n):
    T=lens8[n]; x=rms(H8[23][n,:T].astype(np.float32))*(1+win)
    V=(x@Wv.T).reshape(T,2,256); G=(x@Wq.T).reshape(T,8,512)[:,:,256:]
    outs=np.zeros((8,T,1024),np.float32)
    for h in range(8):
        att=A8[n][h,:T,:T].astype(np.float32)@V[:,h//4]; att=att/(1+np.exp(-G[:,h])); outs[h]=att@Wo[:,h*256:(h+1)*256].T
    return outs
HO8=[head_outputs8(n) for n in range(2)]
HF8=[H8[23][n,:lens8[n]].astype(np.float32)+HO8[n].sum(0)+M8[23][n,:lens8[n]].astype(np.float32)@Wd23.T for n in range(2)]
for n in range(2):
    chk=rms(HF8[n])*(1+wnn); e=np.linalg.norm(chk-H8[24][n,:lens8[n]].astype(np.float32),axis=1)/np.linalg.norm(chk,axis=1); print('recon err', np.median(e).round(4))
def dla_layers(n,p,a,b):
    d=((E[a]-E[b])*(1+wn)).numpy(); r=np.sqrt((HF8[n][p]**2).mean())
    cons=[]; prev=np.zeros(1024,np.float32)
    for l in range(24):
        h=H8[l][n,p].astype(np.float32); cons.append(((h-prev)@d)/r); prev=h
    att=HO8[n][:,p]@d/r; mlp=(M8[23][n,p].astype(np.float32)@Wd23.T)@d/r
    return np.array(cons), att, mlp, (HF8[n][p]@d)/r
pfirst=[[i for i,t in enumerate(ids8[n]) if t==248068][0]+1 for n in range(2)]
for n in range(2):
    for (a,b,name) in [(T_think,T_the,'Thinking-The'),(T_think,T_ok,'Thinking-Okay')]:
        cons,att,mlp,tot=dla_layers(n,pfirst[n],a,b)
        print(f'text{n} {name}: total {tot:.2f} | emb+L0..L22: {np.round(cons,1)} | L23 heads {np.round(att,2)} mlp23 {mlp:.2f}')
```