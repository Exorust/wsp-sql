```python
# Find the most selective 'start-of-thinking' detector neurons in L16-23: high at first position, near-zero elsewhere
cands = []
for l in range(16,24):
    A = Mall[l].astype(np.float32)  # [6,1600,3584]
    first = np.stack([A[n, first_pos[n]] for n in range(6)])   # [6,3584]
    mask = np.zeros((6,1600), bool)
    for n in range(6): mask[n,1:lens7[n]] = True
    for n in range(6): mask[n, first_pos[n]] = False
    rest = A[mask]   # [Nrest,3584]
    fmin = first.min(0); fmean = first.mean(0)
    rmax = np.abs(rest).max(0); r999 = np.percentile(np.abs(rest), 99.9, axis=0); rstd = rest.std(0)
    sel = np.abs(fmin) / (r999 + 1e-3)
    for j in np.argsort(-sel)[:5]:
        cands.append((round(float(sel[j]),2), l, int(j), round(float(fmean[j]),2), round(float(fmin[j]),2), round(float(r999[j]),3), round(float(rmax[j]),3), round(float(rstd[j]),3)))
cands.sort(reverse=True)
print("(selectivity, layer, neuron, first-pos mean, first-pos min, |rest| p99.9, |rest| max, rest std)")
for c_ in cands[:20]: print(c_)
```