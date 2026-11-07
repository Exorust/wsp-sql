```python
# Onset (tokens into the full text incl. prompt?) distribution; and whether a SELECT appears in generation before onset
ons = np.array([a['onset'] for a in setA]); per = np.array([a['period'] for a in setA])
print("onset quantiles", np.percentile(ons,[10,25,50,75,90]).round(), "period quantiles", np.percentile(per,[10,25,50,75,90]).round())
# map id -> gen_1 n_tokens / text
g1d = {r['id']: r for r in g1}
cnt_sel=0; cnt_sql=0; nn=0
for a in setA:
    r = g1d.get(a['id'])
    if r is None: continue
    nn+=1
    gen = r['text']
    # approximate: onset is token index in full text; estimate prompt length tokens
    ids_full = tok.encode(a['text']).ids
    pre = tok.decode(ids_full[:a['onset']])
    gpart = pre.split('<think>')[-1] if '<think>' in pre else pre
    if 'SELECT' in gpart: cnt_sel+=1
    if '```sql' in gpart: cnt_sql+=1
print(nn, "texts; SELECT written before loop onset:", cnt_sel, "; ```sql before onset:", cnt_sql)
```