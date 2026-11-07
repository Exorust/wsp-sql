```python
# Which late-layer neurons suppress </think> (vs 'Thinking') at the first position, consistently over 6 texts?
c = neuron_contrib(d2, posl, range(16,24))
allc = np.concatenate([c[l] for l in range(16,24)])
print("layer sums:", {l: round(float(c[l].sum()),2) for l in c})
bot = np.argsort(allc)[:25]
print("top suppressors of </think>:", [(16+i//3584, int(i%3584), round(float(allc[i]),2)) for i in bot])
top = np.argsort(-allc)[:12]
print("top promoters of </think>:", [(16+i//3584, int(i%3584), round(float(allc[i]),2)) for i in top])
# consistency: per-text contribution for the top 10 suppressors
def per_text(l, i, dv):
    proj = float(Wd_all[l][:, i] @ dv)
    return [round(float(Mall[l][n,q])*proj/float(np.sqrt((H[23][n,q].astype(np.float32)**2).mean())),2) for n,q in posl]
for i in bot[:10]:
    l, j = 16+i//3584, int(i%3584)
    print((l,j), per_text(l,j,d2))
```