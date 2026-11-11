```python
# DLA by layer of logit(Thinking)-logit(The) and logit(</think>)-logit(Thinking) at the position after '<think>\n' (12 loop texts of fwd_5)
E=load('model.language_model.embed_tokens.weight'); wn=load('model.language_model.norm.weight')
def tid(s): 
    i=tok.encode(s).ids; assert len(i)==1, (s,i); return i[0]
T_think=tid('Thinking'); T_the=tid('The'); T_ok=tid('Okay'); T_end=248069
H={l:np.load(f'{W}/fwd_5/hidden_L{l}.npy') for l in range(25)}
pos0=[]
for n in range(12):
    idsn=tok.encode(req['texts'][n]).ids
    pos0.append([i for i,t in enumerate(idsn) if t==thk[-1]][0]+1)   # the '\n' after <think>
def dla(a,b,positions):
    d=((E[a]-E[b])*(1+wn)).numpy()
    out=np.zeros((12,25))
    for n,p in enumerate(positions):
        h24=H[24][n,p].astype(np.float32); rms=np.sqrt((h24**2).mean()+1e-6)
        prev=np.zeros(1024,np.float32)
        for l in range(25):
            h=H[l][n,p].astype(np.float32); out[n,l]=((h-prev)@d)/rms; prev=h
    return out
A=dla(T_think,T_the,pos0); B=dla(T_end,T_think,pos0)
print('Thinking-The by layer (mean over 12):', np.round(A.mean(0),2), 'total', round(A.sum(1).mean(),2))
print('</think>-Thinking by layer:', np.round(B.mean(0),2), 'total', round(B.sum(1).mean(),2))
```