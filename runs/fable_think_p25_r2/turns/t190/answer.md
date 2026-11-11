```python
# Structural comparison pred vs gold over non-cut gen_11 answers: where does the no-think model systematically over/under-generate?
import re
def feats(q):
    q=q.upper()
    sel=q.split('FROM')[0] if 'FROM' in q else q
    return dict(join=q.count(' JOIN '), distinct=int('DISTINCT' in q), group=int('GROUP BY' in q), where=int(' WHERE ' in q),
                notnull=int('IS NOT NULL' in q), ncols=sel.count(',')+1, star=int('SELECT *' in q), limit=int('LIMIT' in q),
                order=int('ORDER BY' in q), sub=q.count('(SELECT')+q.count('( SELECT'), alias=int(' AS ' in q), having=int('HAVING' in q),
                setop=int(any(s in q for s in ['EXCEPT','INTERSECT','UNION'])))
rows=[]
for r in g11:
    if r['id'] not in byid or r['cut']: continue
    fp=feats(r['sql']); fg=feats(byid[r['id']]['gold']); rows.append((r['cls']=='correct',fp,fg))
import pandas as pd
keys=list(rows[0][1].keys())
df=pd.DataFrame([{**{'ok':ok},**{k+'_p':fp[k] for k in keys},**{k+'_g':fg[k] for k in keys}} for ok,fp,fg in rows])
print('n',len(df))
for k in keys:
    print('%-9s pred mean %.2f gold mean %.2f | pred>gold %3d  pred<gold %3d | among wrong: pred>gold %3d pred<gold %3d'%(k,df[k+'_p'].mean(),df[k+'_g'].mean(),(df[k+'_p']>df[k+'_g']).sum(),(df[k+'_p']<df[k+'_g']).sum(),((df[k+'_p']>df[k+'_g'])&~df.ok).sum(),((df[k+'_p']<df[k+'_g'])&~df.ok).sum()))
```