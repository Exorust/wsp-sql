```python
# Compute instruction-effect directions at layers 10..18: diff of hidden states V1-V0 at aligned assistant positions
H13={L:np.load(os.path.join(F13,f'hidden_L{L}.npy')) for L in [10,12,14,16,18]}
print({L:H13[L].shape for L in H13})
def assistant_start(text):  # index of '<|im_start|>assistant' token
    s=text.rfind('<|im_start|>assistant'); return len(tok.encode(text[:s]).ids)
AS13=[assistant_start(t) for t in T13]
dirs={}
for L in H13:
    H=H13[L].astype(np.float32)
    dsel=[];dall=[];dpre=[]; rms=[]
    for i in range(N):
        a,b=i,i+N; sa,sb=ST13[a],ST13[b]; la=LEN13[a]
        n=la-sa
        dsel.append(H[b,sb]-H[a,sa])                       # at 'SELECT' token
        dall.append((H[b,sb:sb+n-1]-H[a,sa:sa+n-1]).mean(0))  # all SQL tokens
        pa,pb=AS13[a],AS13[b]; m=sa-pa
        dpre.append((H[b,pb:pb+m]-H[a,pa:pa+m]).mean(0))   # assistant prefix tokens
        rms.append(np.sqrt((H[a,sa:la]**2).mean()))
    dsel=np.array(dsel); dall=np.array(dall); dpre=np.array(dpre)
    msel=dsel.mean(0); mall=dall.mean(0); mpre=dpre.mean(0)
    cos=lambda u,v: float(u@v/np.linalg.norm(u)/np.linalg.norm(v))
    # consistency: cosine of each problem's dsel with the mean
    cons=np.mean([cos(dsel[i],msel) for i in range(N)])
    print(f'L{L}: resid RMS {np.mean(rms):.3f} | |mean dsel| {np.linalg.norm(msel):.3f} |mean dall| {np.linalg.norm(mall):.3f} |mean dpre| {np.linalg.norm(mpre):.3f} | cos(sel,all) {cos(msel,mall):.2f} cos(sel,pre) {cos(msel,mpre):.2f} | per-problem cos to mean {cons:.2f}')
    dirs[L]=dict(sel=msel, all=mall, pre=mpre)
```