```python
# Hypothesis: the loop locks in progressively; look at per-repetition mean logprob and the alternatives at the loop start
def rep_stats(ti, ids, P, start):
    T=len(ids); l=lp[ti,:T]
    k=0
    while start+(k+1)*P<=T:
        seg=l[start+k*P:start+(k+1)*P]
        print(f' rep {k}: mean lp {np.nanmean(seg):.3f} min {np.nanmin(seg):.2f} n<-1: {(seg<-1).sum()}')
        k+=1
print('text0'); rep_stats(0, ids0, 89, 604)
print('text1'); rep_stats(1, ids1, 35, 1016)
# tokens with lowest logprob in the generated part of text0 (beyond prompt)
pl0=155; pl1=440
tk_ids=np.load(F+'/topk_ids.npy'); tk_lp=np.load(F+'/topk_logprobs.npy')
def worst(ti, ids, pl, n=15):
    T=len(ids); l=lp[ti,:T].copy(); l[:pl]=0
    order=np.argsort(l)[:n]
    for p in sorted(order):
        ctx=tok.decode(ids[max(p-8,0):p]); nxt=tok.decode([ids[p]])
        alts=[(tok.decode([int(a)]),round(float(b),2)) for a,b in zip(tk_ids[ti,p-1,:4],tk_lp[ti,p-1,:4])]
        print(p, f'{l[p]:.2f}', repr(ctx[-40:]), '->', repr(nxt), alts)
worst(0, ids0, pl0)
```