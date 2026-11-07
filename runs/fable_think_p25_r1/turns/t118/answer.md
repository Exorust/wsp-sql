```python
# Find late-layer MLP neurons selectively active at the '\n' right after '<think>' (the first-thinking-token decision position)
pos_think = [ids7[i].index(think_id)+1 for i in range(6)]   # index of '\n' after <think>
lens7 = [len(x) for x in ids7]
cands=[]
for L in range(16,24):
    A = M[L]  # (6,T,3584) float16
    at = np.stack([A[i,pos_think[i]].astype(np.float32) for i in range(6)])  # (6,3584)
    # other positions: all valid positions except pos_think
    other_max = np.zeros(3584, dtype=np.float32)
    for i in range(6):
        a = np.abs(A[i,:lens7[i]].astype(np.float32)); a[pos_think[i]] = 0
        other_max = np.maximum(other_max, np.percentile(a, 99.9, axis=0))
    sel = np.abs(at).min(0) / (other_max+1e-3)
    for j in np.argsort(-sel)[:4]:
        cands.append((L,int(j), float(sel[j]), at[:,j].round(1).tolist(), float(other_max[j])))
cands.sort(key=lambda x:-x[2])
for c in cands[:12]: print(c)
```