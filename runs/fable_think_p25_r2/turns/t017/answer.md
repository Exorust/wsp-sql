```python
# Hypothesis: same as before; fix key access (err may be missing in some rows)
stats=[]
for r in rows:
    p,s=loop_info(r['text'])
    stats.append((r['id'],p,s,r['n_tokens'],r['cls'],(r.get('err') or '')[:40]))
df=pd.DataFrame(stats,columns=['id','period','start','ntok','cls','err'])
print(df[['period','start']].describe())
print('no period',df['period'].isna().sum(),'no start',df['start'].isna().sum())
print(df['cls'].value_counts())
print(df.head(12))
```