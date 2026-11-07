```python
# Characterize candidate </think>-promoter neurons L22n1936, L23n442: where do they fire (across the 6 fwd_7 texts)?
lens7 = [1566,1600,1600,1600,1317,1298]
ids7 = [tok.encode(t).ids for t in texts7]
def profile(l, j, k=8):
    a = Mall[l][:, :, j].astype(np.float32)
    vals = np.concatenate([a[n,:lens7[n]] for n in range(6)])
    print(f"L{l}n{j}: mean {vals.mean():.3f} std {vals.std():.3f} min {vals.min():.3f} max {vals.max():.3f}; at first pos: {[round(float(a[n,first_pos[n]]),3) for n in range(6)]}")
    # top-k positions by |act| (sign that matches direction)
    proj = float(Wd_all[l][:, j] @ d2)
    sgn = np.sign(proj)
    flat = [(sgn*a[n,q], n, q) for n in range(6) for q in range(1,lens7[n])]
    flat.sort(reverse=True)
    for v,n,q in flat[:k]:
        print("   ", round(float(v),2), repr(tok.decode(ids7[n][max(0,q-10):q+1]))[-70:], "-> next:", repr(tok.decode([ids7[n][q+1]])) if q+1<lens7[n] else "")
    print("   proj onto (</think>-Thinking):", round(proj,3), " proj onto </think> unembed only:", round(float(Wd_all[l][:, j] @ (gN*E[ID_TC])),3))
profile(22,1936); profile(23,442)
```