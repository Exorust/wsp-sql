```python
# Track p('\n') vs p('\n\n') at each end-of-bullet position across the text (before/after loop onset)
NL=198; NL2=271
def eol_positions(ids):
    # positions t where ids[t]==NL (single newline) and previous token ends a sentence
    return [t for t in range(1,len(ids)) if ids[t] in (NL,NL2)]
for ti in range(2):
    ids=np.array(toks[ti]); T=len(ids)
    print("text",ti)
    for t in eol_positions(ids):
        row_ids=tk[ti,t]; row_lp=tlp[ti,t]
        d={int(i):float(l) for i,l in zip(row_ids,row_lp)}
        p1=np.exp(d.get(NL,-30)); p2=np.exp(d.get(NL2,-30))
        # also show what follows the newline actually and the top alternative tokens after \n\n
        prev=tok.decode(ids[max(0,t-6):t]).replace('\n','\\n')
        print(f"t={t:4d} actual={'NL ' if ids[t]==NL else 'NL2'} p(NL)={p1:.3f} p(NL2)={p2:.3f}  prev={prev!r}")
```