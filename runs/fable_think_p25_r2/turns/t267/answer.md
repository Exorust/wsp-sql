```python
# (fix indexing: topk[j,q] predicts token q+1) re-measure DISTINCT after SELECT and alias/JOIN after FROM table
stats=[]
for j in range(32):
    enc=tok.encode(T[j]); offs=enc.offsets; toks=[T[j][x:y] for x,y in offs]; a0,b0,_=my_sql_span(T[j])
    for p in range(a0,b0):
        if toks[p].strip().upper()=='SELECT':
            row=dict(zip(tk_ids[j,p].tolist(),tk_lp[j,p].tolist()))
            pd=max([row.get(t,-99) for t in tid(' DISTINCT')+tid(' distinct')])
            stats.append(('SEL',j,repr(toks[p+1]),round(pd,2),round(float(lp[j,p+1]),2),show_top(j,p,3))); break
    for p in range(a0,b0):
        if toks[p].strip().upper()=='FROM':
            q=p+2
            while q<b0 and not toks[q].startswith(' '): q+=1
            if q<b0:
                row=dict(zip(tk_ids[j,q-1].tolist(),tk_lp[j,q-1].tolist()))
                pj=max([row.get(t,-99) for t in tid(' JOIN')]); pa=max([row.get(t,-99) for t in tid(' AS')])
                stats.append(('FROM',j,repr(toks[q]),round(pj,2),round(pa,2),round(float(lp[j,q]),2),show_top(j,q-1,3)))
            break
for s in stats: print(s)
```