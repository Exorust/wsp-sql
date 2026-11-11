```python
# Redo with whitespace normalized
def feats(q):
    q=re.sub(r'\s+',' ',q.upper())
    sel=q.split(' FROM ')[0] if ' FROM ' in q else q
    return dict(join=q.count(' JOIN '), distinct=int('DISTINCT' in q), group=int('GROUP BY' in q), where=int(' WHERE ' in q),
                notnull=int('IS NOT NULL' in q), ncols=sel.count(',')+1, star=int('SELECT *' in q), limit=int('LIMIT' in q),
                order=int('ORDER BY' in q), sub=q.count('(SELECT')+q.count('( SELECT'), having=int('HAVING' in q),
                setop=int(any(s in q for s in ['EXCEPT','INTERSECT','UNION'])), eq1=int(bool(re.search(r'= 1\b',q))))
rows=[]
for r in g11:
    if r['id'] not in byid or r['cut']: continue
    fp=feats(r['sql']); fg=feats(byid[r['id']]['gold']); rows.append((r['cls']=='correct',fp,fg,r['cls']))
keys=list(rows[0][1].keys())
df=pd.DataFrame([{**{'ok':ok,'cls':c},**{k+'_p':fp[k] for k in keys},**{k+'_g':fg[k] for k in keys}} for ok,fp,fg,c in rows])
print('n',len(df))
for k in keys:
    print('%-9s pred mean %.2f gold mean %.2f | pred>gold %3d  pred<gold %3d | among wrong: pred>gold %3d pred<gold %3d'%(k,df[k+'_p'].mean(),df[k+'_g'].mean(),(df[k+'_p']>df[k+'_g']).sum(),(df[k+'_p']<df[k+'_g']).sum(),((df[k+'_p']>df[k+'_g'])&~df.ok).sum(),((df[k+'_p']<df[k+'_g'])&~df.ok).sum()))
# accuracy by gold join count
print(df.groupby('join_g').ok.agg(['mean','count']))
```