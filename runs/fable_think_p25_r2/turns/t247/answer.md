```python
# V1 top-3 at the correct SELECT position; and where in the SQL do the gains come from (position within SQL)
def topk13(i,j,k=3): return [(S(tok.decode([int(t)])),round(float(l),2)) for t,l in zip(tk13[i,j,:k],tkl13[i,j,:k])]
for i in range(0,N,2):
    a,b=i,i+N
    print(pool[i], 'V0 top', topk13(a,ST13[a]), '| V1 top', topk13(b,ST13[b]))
# per-token-position gains
gain_by_pos=collections.defaultdict(list)
for i in range(N):
    a,b=i,i+N
    s0=lp13[a,ST13[a]+1:LEN13[a]-1]; s1=lp13[b,ST13[b]+1:LEN13[b]-1]
    for p,(x,y) in enumerate(zip(s0,s1)): gain_by_pos[min(p,8)].append(y-x)
print({p:(round(float(np.mean(v)),2),len(v)) for p,v in sorted(gain_by_pos.items())})
```