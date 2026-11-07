```python
# What does the model predict right after '<think>\n'? Is '</think>' a contender at the very start?
for n in range(6):
    ids = tok.encode(texts7[n]).ids
    q = ids.index(248068)  # <think>
    print(n, repr(tok.decode(ids[q:q+4])))
    for s in [q, q+1, q+2]:
        print("   after", repr(tok.decode([ids[s]])), "->", [(tok.decode([int(i)]), round(float(l),2)) for i,l in zip(tk7[n,s], tkl7[n,s])][:6])
```