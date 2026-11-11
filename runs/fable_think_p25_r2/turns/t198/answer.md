```python
# Pick ~40 short gold texts (<=2 per db) for a compact teacher-forced request; print in chunks later
cand=[p for p in probs if p['id'] not in exclude]
cand=sorted(cand,key=lambda p: len(t2_text(p)))
per_db={}; setB=[]
for p in cand:
    if per_db.get(p['db'],0)>=2: continue
    per_db[p['db']]=per_db.get(p['db'],0)+1; setB.append(p)
    if len(setB)>=40: break
textsB=[t2_text(p) for p in setB]
toks=[len(tok.encode(t).ids) for t in textsB]
print('n',len(textsB),'total tokens',sum(toks),'max',max(toks),'chars',sum(len(t) for t in textsB),'dbs',len(per_db))
print('gold join share',np.mean([' JOIN ' in p['gold'].upper() for p in setB]),'distinct',np.mean(['DISTINCT' in p['gold'].upper() for p in setB]),'where',np.mean([' WHERE ' in p['gold'].upper() for p in setB]))
for p in setB[:40]: print(p['id'], p['gold'][:90])
```