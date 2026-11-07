```python
# Distribution of bullet-end margins (nl - nlnl) in loop texts; which bullets are soft?
for i in [1,2,3,5]:
    d=de[(de.i==i)&(de.chosen=='nl')]
    print(i, 'quantiles', np.percentile(d.margin,[10,25,50,75]).round(2), 'n<2:', int((d.margin<2).sum()), 'n', len(d))
    soft=d[d.margin<2.5].sort_values('margin')[:4]
    for r in soft.itertuples():
        print('   m=%.2f'%r.margin, repr(tok.decode(enc[i][r.j-14:r.j])))
```