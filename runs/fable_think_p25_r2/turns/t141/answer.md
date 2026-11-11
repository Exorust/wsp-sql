```python
# Verify indexing: topk at position p predicts token p+1. Check predictions at '<think>' and '\n' positions
for i in [0,3,6]:
    ids=ids3[i]; pos=[p for p,x in enumerate(ids) if x==248068][0]
    for p in [pos, pos+1]:
        print(i, repr(tok.decode([ids[p]])), '->', [(tok.decode([int(a)])[:12], round(float(b),2)) for a,b in zip(tk3[i,p], tl3[i,p])], '| actual next', repr(tok.decode([ids[p+1]])), round(float(lp3[i,p+1]),2))
```