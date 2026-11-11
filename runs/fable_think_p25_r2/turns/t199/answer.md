```python
# Stratified selection of short texts by gold structure
cand=[p for p in probs if p['id'] not in exclude and len(sch(p['db']))<=800]
def kind(g):
    u=re.sub(r'\s+',' ',g.upper())
    if ' JOIN ' in u: return 'join'
    if 'GROUP BY' in u: return 'group'
    if 'ORDER BY' in u: return 'order'
    if ' WHERE ' in u and '(SELECT' not in u: return 'where'
    if 'COUNT(*)' in u: return 'count'
    return 'plain'
random.seed(3); random.shuffle(cand)
quota={'join':12,'group':8,'order':8,'where':10,'plain':8,'count':2}
setB=[]; per_db={}
for p in cand:
    k=kind(p['gold'])
    if quota.get(k,0)<=0 or per_db.get(p['db'],0)>=3: continue
    quota[k]-=1; per_db[p['db']]=per_db.get(p['db'],0)+1; setB.append(p)
textsB=[t2_text(p) for p in setB]
toks=[len(tok.encode(t).ids) for t in textsB]
print('n',len(textsB),'total tokens',sum(toks),'max',max(toks),'chars',sum(len(t) for t in textsB),'dbs',len(per_db), quota)
for p in setB: print(p['id'], kind(p['gold']), p['gold'][:100])
```