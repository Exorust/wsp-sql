```python
# Decompose layer 23 (last) contribution into attention vs MLP at decision positions
Wd23=load_original("model.language_model.layers.23.mlp.down_proj.weight").numpy()  # (1024,3584)
M23=np.load(f"{F2}/mlp_down_in_L23.npy")
def split23(ti,t):
    x_final=H[24][ti,t-1].astype(np.float32); rms=np.sqrt((x_final**2).mean()+1e-6)
    total=(H[24][ti,t-1].astype(np.float32)-H[23][ti,t-1].astype(np.float32))
    mlp=Wd23@M23[ti,t-1].astype(np.float32)
    attn=total-mlp
    return float(total@u_dir/rms), float(mlp@u_dir/rms), float(attn@u_dir/rms)
for t in dec[::3]:
    tot,m,a=split23(0,t); print(t, "total=%.2f mlp=%.2f attn=%.2f"%(tot,m,a))
# also text 1
ids1=np.array(toks[1]); dec1=[t for t in eol_positions(ids1) if t>1000]
print("text1")
for t in dec1[::2]:
    tot,m,a=split23(1,t); d=dist_at(1,t); print(t, "logitdiff=%.2f total=%.2f mlp=%.2f attn=%.2f"%(d.get(NL,-30)-d.get(NL2,-30),tot,m,a))
```