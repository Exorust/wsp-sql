```python
# Build loop-text set: for each gen_1 answer, find token-level loop start/period; keep texts whose prompt+thinking up to start+3 periods <= ~750 tokens
def tok_loop(tt, minP=8, maxP=200, reps=2):
    # find earliest position s and period P such that tt[s:s+P*reps] is periodic with period P
    n=len(tt)
    for s in range(0, n-minP*reps):
        for Pp in range(minP, maxP):
            if s+Pp*(reps+1)>n: break
            ok=True
            for k in range(1,reps+1):
                if tt[s:s+Pp]!=tt[s+Pp*k:s+Pp*(k+1)]: ok=False;break
            if ok: return s,Pp
    return None,None
cands=[]
for r in G:
    tt=tok.encode(r['text'][:12000]).ids
    s,Pp=tok_loop(tt)
    if s is None: continue
    pl=len(tok.encode(raw_text(r['id'],'')).ids)
    cands.append((r['id'],pl,s,Pp,pl+s+3*Pp))
print(len(cands)); print(sorted(c[4] for c in cands)[:40])
```