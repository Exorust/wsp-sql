```python
# Same as before, avoid triple backticks in code (use FENCE)
FENCE = "`"*3
ons = np.array([a['onset'] for a in setA]); per = np.array([a['period'] for a in setA])
print("onset quantiles", np.percentile(ons,[10,25,50,75,90]).round(), "period quantiles", np.percentile(per,[10,25,50,75,90]).round())
g1d = {r['id']: r for r in g1}
cnt_sel=0; cnt_sql=0; nn=0; onset_gen=[]
for a in setA:
    ids_full = tok.encode(a['text']).ids
    pre = tok.decode(ids_full[:a['onset']])
    if '<think>' not in pre: continue
    nn+=1
    gpart = pre.split('<think>')[-1]
    onset_gen.append(len(tok.encode(gpart).ids))
    if 'SELECT' in gpart: cnt_sel+=1
    if FENCE+'sql' in gpart: cnt_sql+=1
print(nn, "texts; SELECT written before loop onset:", cnt_sel, "; sql fence before onset:", cnt_sql)
print("gen tokens before onset quantiles", np.percentile(onset_gen,[10,25,50,75,90]).round())
```