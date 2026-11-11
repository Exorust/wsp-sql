```python
# What does the model predict after SELECT and after FROM <table> in gold chats? (formatting vs semantics)
def show_top(j,q,k=5):
    return [(repr(tok.decode([int(t)])),round(float(l),2)) for t,l in zip(tk_ids[j,q][:k],tk_lp[j,q][:k])]
for j in [1,2,6,12,15]:
    enc=tok.encode(T[j]); offs=enc.offsets; toks=[T[j][x:y] for x,y in offs]; a0,b0,_=my_sql_span(T[j])
    for p in range(a0,b0):
        if toks[p].strip().upper()=='SELECT':
            print(j,'after SELECT -> gold',repr(toks[p+1]), show_top(j,p+1)); break
    for p in range(a0,b0):
        if toks[p].strip().upper()=='FROM':
            q=p+2
            while q<b0 and not toks[q].startswith(' '): q+=1
            if q<b0: print(j,'after FROM tbl -> gold',repr(toks[q]), show_top(j,q))
            break
```