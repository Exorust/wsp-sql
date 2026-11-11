```python
for i in range(6):
    t=ids[i]; d=meta['loop'][i]
    rows=[]
    for p in range(d['pl']+1,d['end']):
        if t[p]==N1[0]:
            rows.append((p, 'L' if p>=d['start'] else 'p', alt_lp(tk3,tp3,i,p-1,nn_id), alt_lp(tk4,tp4,i,p-1,nn_id), float(lp3[i,p]), float(lp4[i,p])))
    print(d['pid'], [(r[0],r[1], None if r[2] is None else round(r[2],1), None if r[3] is None else round(r[3],1)) for r in rows[-9:]])
```