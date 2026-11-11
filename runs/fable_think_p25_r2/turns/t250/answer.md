```python
# Per-position profile of the instruction effect within the SQL (layer 14): norm and cosine to the SELECT-position direction
for L in [12,14,16]:
    H=H13[L].astype(np.float32); msel=dirs[L]['sel']
    prof=collections.defaultdict(list)
    for i in range(N):
        a,b=i,i+N; sa,sb=ST13[a],ST13[b]; n=LEN13[a]-sa
        for p in range(-6,n):
            d=H[b,sb+p]-H[a,sa+p]; prof[p].append((np.linalg.norm(d), d@msel/np.linalg.norm(d)/np.linalg.norm(msel)))
    print('L',L, ' pos:(norm,cos)', {p:(round(float(np.mean([x[0] for x in v])),2), round(float(np.mean([x[1] for x in v])),2)) for p,v in sorted(prof.items()) if p<=10})
```