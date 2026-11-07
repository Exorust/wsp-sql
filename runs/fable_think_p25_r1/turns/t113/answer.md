```python
# Neuron-level logit-lens: contributions to d=(</think> - indent) direction at exit vs comparison positions, layers 16-23
M = {L: np.load(D7+f"/mlp_down_in_L{L}.npy") for L in range(16,24)}
DP = {L: load_original(f"model.language_model.layers.{L}.mlp.down_proj.weight") for L in range(16,24)}
dd = {L: (d @ DP[L]).numpy() for L in range(16,24)}   # (3584,) per-neuron output alignment with d
def rms23(i,p): return float((H[23][i,p].astype(np.float32)**2).mean()**0.5)
def contrib(i,p,L): return M[L][i,p].astype(np.float32)*dd[L]/rms23(i,p)
print("layer | sum contrib exit | mean sum contrib cmp")
tops={}
for L in range(16,24):
    ce = contrib(0,exit_p,L); cc = np.mean([contrib(0,q,L) for q in cmp],axis=0)
    print(L, f"{ce.sum():.2f} {cc.sum():.2f}")
    # top neurons by exit-vs-cmp difference, and top negative neurons at cmp (indent drivers)
    diff = ce-cc
    ti = np.argsort(-diff)[:5]; tn = np.argsort(cc)[:5]
    print("   exit-promoting (j, exit, cmp):", [(int(j), round(float(ce[j]),2), round(float(cc[j]),2)) for j in ti])
    print("   indent-promoting at cmp (j, exit, cmp):", [(int(j), round(float(ce[j]),2), round(float(cc[j]),2)) for j in tn])
```