```python
# Constructed texts: lp(</think>) at the forced exit, competitor tokens, and quality of the SQL after exit
for i in [4,5]:
    ids_i = ids7[i]; pe = ids_i.index(TT)
    print(info[i], "exit at", pe, repr(tok.decode(ids_i[pe-10:pe])))
    print("  prev-step: lp of actual '\\n'", round(float(lp7[i,pe-1]),2), "top:", [(tokstr(ti7[i,pe-2,k]), round(float(tl7[i,pe-2,k]),1)) for k in range(5)])
    print("  lp(</think>)", round(float(lp7[i,pe]),2), "top:", [(tokstr(ti7[i,pe-1,k]), round(float(tl7[i,pe-1,k]),1)) for k in range(6)])
    # after exit: the answer tokens
    T=len(ids_i); ans=ids_i[pe+1:]
    print("  answer lp per token:", [ (tokstr(ids_i[q]), round(float(lp7[i,q]),1)) for q in range(pe+1, T)][:30])
```