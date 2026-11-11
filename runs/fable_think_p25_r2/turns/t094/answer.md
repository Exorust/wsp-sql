```python
# Hypothesis: thinking structure is uniform; check how answers start and whether length of schema matters
pr='/Users/chandu/myproj/wsp-sql/practice'
sch={}
def schema(db):
    if db not in sch: sch[db]=open(f'{pr}/schemas/{db}.sql').read()
    return sch[db]
slen=[len(tok.encode(schema(r['db'])).ids) for r in g1]
hasSel=[('SELECT' in r['text']) for r in g1]
print('schema tokens: min/median/max', min(slen), int(np.median(slen)), max(slen))
print('SELECT present by schema len quartile:')
q=np.quantile(slen,[0,.25,.5,.75,1])
for i in range(4):
    m=[(slen[j]>=q[i]) and (slen[j]<=q[i+1]) for j in range(128)]
    print(f'  {int(q[i])}-{int(q[i+1])}: n={sum(m)} hasSelect={np.mean([hasSel[j] for j in range(128) if m[j]]):.2f}')
for r in g1[:3]:
    print('----', r['id'], r['db'], 'schema toks', len(tok.encode(schema(r['db'])).ids))
    print(r['text'][:700].replace('\n','\\n'))
```