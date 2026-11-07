```python
# Check alignment: topk at p-1 should contain </think>; and what competed with it
p = pos[0]
for q in [p-2, p-1, p]:
    print(q, repr(tok.decode([ids0[q]])), "->", [(tok.decode([int(i)]), round(float(l),2)) for i,l in zip(tk7[0,q], tkl7[0,q])][:6])
# texts 4 and 5 also contain </think>: check
for n in [4,5]:
    ids = tok.encode(texts7[n]).ids
    ps = [i for i,x in enumerate(ids) if x==TH[0]]
    for q in ps:
        print(n, q, repr(tok.decode(ids[q-10:q+3])), "lp", lp7[n,q], "top at q-1:", [(tok.decode([int(i)]), round(float(l),2)) for i,l in zip(tk7[n,q-1], tkl7[n,q-1])][:5])
```