```python
# Does alias-prefixed SELECT style correlate with failure, especially on gold-0-join questions?
def style(sql):
    s=re.sub(r'\s+',' ',(sql or '').strip())
    m=re.match(r'SELECT (DISTINCT )?(\w+)\.',s)
    if m: return 'alias'
    if re.match(r'SELECT (DISTINCT )?(COUNT|SUM|AVG|MIN|MAX)\(',s,re.I): return 'agg'
    if s.startswith('SELECT *'): return 'star'
    return 'bare'
rows=[]
for r in g11:
    if r['id'] not in byid: continue
    g=byid[r['id']]['gold']; rows.append(dict(ok=r['cls']=='correct',style=style(r['sql']),gjoin=feats(g)['join'],distinct=('DISTINCT' in (r['sql'] or '').upper()),cut=r['cut']))
dfs=pd.DataFrame(rows)
print(dfs.groupby(['gjoin','style']).ok.agg(['mean','count']).round(2))
print(dfs.groupby(['distinct']).ok.agg(['mean','count']).round(2))
print(dfs[dfs.gjoin==0].groupby(['distinct']).ok.agg(['mean','count']).round(2))
```