```python
# At the token right after 'SELECT' in gold chats: model's top-5 (does it prefer alias/DISTINCT style?)
res=[]
for i in range(36):
    ids=tok.encode(texts[i]).ids; toks=[tok.decode([t]) for t in ids]
    s=texts[i].rfind(FENCE+'sql\n'); pos=0; start=None
    for j,t in enumerate(toks):
        pos+=len(t)
        if start is None and pos>s+7: start=j
    if start is None: continue
    for j in range(start,len(ids)-1):
        if toks[j].strip().upper()=='SELECT':
            res.append((meta_ids[i], S(repr(toks[j+1])), round(float(lp[i,j+1]),2), topk_at(i,j,5)))
            break
for r in res: print(r[0], 'gold', r[1], r[2], '| top', r[3])
```