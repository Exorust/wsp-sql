```python
# DLA at first thinking token: which late-layer MLP neurons promote 'Thinking' over 'Okay'/'The'? (uses fwd_7 activations at the '\n' after <think>)
ID_THINKING = tok.encode("Thinking").ids[0]; ID_OKAY = tok.encode("Okay").ids[0]; ID_THE = tok.encode("The").ids[0]; ID_LET = tok.encode("Let").ids[0]
print(ID_THINKING, ID_OKAY, ID_THE, ID_LET)
Mall = {l: np.load(f"{W}/fwd_7/mlp_down_in_L{l}.npy") for l in range(16,24)}
Wd_all = {l: load_original(f"model.language_model.layers.{l}.mlp.down_proj.weight") for l in range(16,24)}
first_pos = []
for n in range(6):
    ids = tok.encode(texts7[n]).ids
    q = ids.index(248068)+1   # the '\n' token after <think>
    first_pos.append(q)
def neuron_contrib(dirvec, positions, layers):
    # returns per-layer array [3584] of mean contribution act_i * (Wd[:,i]·dir) / rms  over positions
    out = {}
    for l in layers:
        proj = (Wd_all[l].T @ dirvec).numpy()   # [3584]
        acc = np.zeros(3584)
        for n,q in positions:
            rms = float(np.sqrt((H[23][n,q].astype(np.float32)**2).mean()))
            acc += Mall[l][n,q].astype(np.float32) * proj / rms
        out[l] = acc/len(positions)
    return out
posl = [(n,first_pos[n]) for n in range(6)]
for alt, name in [(ID_OKAY,'Okay'), (ID_THE,'The')]:
    dv = gN*(E[ID_THINKING]-E[alt])
    c = neuron_contrib(dv, posl, range(16,24))
    print(f"--- 'Thinking' minus '{name}': layer sums", {l: round(float(c[l].sum()),2) for l in c})
    allc = np.concatenate([c[l] for l in range(16,24)])
    top = np.argsort(-allc)[:15]
    print("  top promoters (layer,neuron,contrib):", [(16+i//3584, int(i%3584), round(float(allc[i]),2)) for i in top])
    bot = np.argsort(allc)[:8]
    print("  top suppressors:", [(16+i//3584, int(i%3584), round(float(allc[i]),2)) for i in bot])
```