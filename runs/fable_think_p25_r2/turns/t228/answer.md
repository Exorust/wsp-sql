```python
# skip ungraded custom-prompt rows
rows_g=[r for r in rows if r['id'] in prob]
tab=[]
for r in rows_g:
    g=feats(prob[r['id']]['gold']); p=feats(r['sql'] or '')
    tab.append(dict(id=r['id'],cls=r['cls'],gj=g['join'],pj=p['join'],gw=g['where'],pw=p['where'],gd=g['distinct'],pd=p['distinct'],gnj=g['njoin'],pnj=p['njoin'],gna=g['nand'],pna=p['nand'],gnc=g['ncol'],pnc=p['ncol']))
df=pd.DataFrame(tab); df['correct']=(df.cls=='correct')
print(len(df), 'acc %.3f'%df.correct.mean())
print('gold JOIN %.2f pred JOIN %.2f | gold WHERE %.2f pred WHERE %.2f | gold DISTINCT %.2f pred DISTINCT %.2f'%(df.gj.mean(),df.pj.mean(),df.gw.mean(),df.pw.mean(),df.gd.mean(),df.pd.mean()))
print('mean #JOIN gold %.2f pred %.2f | mean #AND gold %.2f pred %.2f | mean #cols gold %.2f pred %.2f'%(df.gnj.mean(),df.pnj.mean(),df.gna.mean(),df.pna.mean(),df.gnc.mean(),df.pnc.mean()))
print(pd.crosstab(df.gj, df.pj, rownames=['goldJOIN'], colnames=['predJOIN']))
print(pd.crosstab(df.gw, df.pw, rownames=['goldWHERE'], colnames=['predWHERE']))
print(df.groupby(['gj','pj']).correct.agg(['mean','count']))
print(df.groupby(['gw','pw']).correct.agg(['mean','count']))
```