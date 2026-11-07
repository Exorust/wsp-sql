```python
# Direct logit attribution per layer for the decision (NL vs NL2) at bullet-end positions in text 0
E=load_original("model.language_model.embed_tokens.weight")  # tied output
gN=load_original("model.language_model.norm.weight")
u_dir=((E[NL]-E[NL2])*gN).numpy()   # direction in pre-norm space (times final norm weight)
H=[np.load(f"{F2}/hidden_L{l}.npy") for l in range(25)]
print(H[0].shape)
def dla(ti, t):
    # contributions of each layer's delta at position t-1 (which predicts token t) to logit(NL)-logit(NL2)
    x_final=H[24][ti,t-1].astype(np.float32)
    rms=np.sqrt((x_final**2).mean()+1e-6)
    contrib=[]
    for l in range(1,25):
        d=(H[l][ti,t-1].astype(np.float32)-H[l-1][ti,t-1].astype(np.float32))
        contrib.append(float(d@u_dir/rms))
    emb=float(H[0][ti,t-1].astype(np.float32)@u_dir/rms)
    return emb, np.array(contrib)
ids0=np.array(toks[0])
dec=[t for t in eol_positions(ids0) if t>740]
rows=[]
for t in dec:
    emb,c=dla(0,t); rows.append(c)
    d=dist_at(0,t); print(t, "logitdiff(NL-NL2)=%.2f"%(d.get(NL,-30)-d.get(NL2,-30)), "emb=%.2f"%emb, "sum=%.2f"%c.sum(), "top layers:", np.argsort(-np.abs(c))[:5]+1, np.round(c[np.argsort(-np.abs(c))[:5]],2))
```