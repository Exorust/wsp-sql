```python
# At soft bullet-end points (margin nl-nlnl < 3), which neurons oppose '\n\n' most? Is there a '\n\n'-suppressor analogous to the digit ones?
soft_pts=[(r.i,r.j) for r in de[(de.margin<3)].itertuples()]
print('n soft points',len(soft_pts))
agg={}
for (i,j) in soft_pts:
    for L in range(16,24):
        c=neuron_contrib(L,i,j-1,198,271)   # positive = toward '\n'
        for n in np.argsort(-c)[:5]:
            agg.setdefault((L,int(n)),[]).append(float(c[n]))
rank=sorted(agg.items(), key=lambda kv:-np.sum(kv[1]))[:12]
for (L,n),v in rank:
    print(f'L{L}n{n}: appears in top5 at {len(v)}/{len(soft_pts)} pts, mean contrib {np.mean(v):.2f}')
```