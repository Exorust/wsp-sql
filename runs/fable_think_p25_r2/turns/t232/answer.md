```python
# Fix SQL start detection via prefix tokenization; redo SELECT-position and FROM-position analyses
def sql_start(text):
    s=text.rfind(FENCE+'sql\n'); return len(tok.encode(text[:s+7]).ids)
TOKS=[]; IDS=[]; STARTS=[]
for i in range(36):
    ids=tok.encode(texts[i]).ids; IDS.append(ids); TOKS.append([tok.decode([t]) for t in ids]); STARTS.append(sql_start(texts[i]))
print([S(repr(t)) for t in TOKS[3][STARTS[3]-2:STARTS[3]+4]])
res=[]
for i in range(36):
    toks=TOKS[i]; st=STARTS[i]
    for j in range(st,len(toks)-1):
        if toks[j].strip().upper()=='SELECT':
            res.append((meta_ids[i], S(repr(toks[j+1])), round(float(lp[i,j+1]),2), topk_at(i,j,4))); break
for r in res: print(r[0], 'gold', r[1], r[2], '| top', r[3])
```