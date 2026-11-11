```python
# Avoid literal triple backticks in code: build the fence string from chr(96)
FENCE=chr(96)*3
def S(x): return str(x).replace(chr(96),'\u02cb')
def analyze(i, show=True, maxshow=14):
    ids=tok.encode(texts[i]).ids; L=len(ids)
    toks=[tok.decode([t]) for t in ids]
    s=texts[i].rfind(FENCE+'sql\n')
    pos=0; start=None
    for j,t in enumerate(toks):
        pos+=len(t)
        if start is None and pos>s+7: start=j
    out=[]
    for j in range(start, L-1):
        gold=ids[j+1]; top=tk[i,j,0]
        if gold!=top:
            out.append((j, toks[j+1], tok.decode([int(top)]), float(lp[i,j+1]), float(tkl[i,j,0])))
    if show:
        print('---',meta_ids[i], 'nSQLtoks', L-start, 'mismatches', len(out))
        for o in out[:maxshow]: print('   gold %s (lp %.2f)  vs top %s (%.2f)'%(S(repr(o[1])),o[3],S(repr(o[2])),o[4]))
    return out
for i in range(6): analyze(i)
```