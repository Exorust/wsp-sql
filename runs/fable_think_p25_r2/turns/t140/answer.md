```python
# At the first generated position (after '<think>','\n'), what are the top-5 candidates and </think>'s logprob?
for i in range(6):
    ids=ids3[i]; pos=[p for p,x in enumerate(ids) if x==248068][0]
    p=pos+2  # predicts token after '<think>','\n'
    print(i, [tok.decode([ids[q]]) for q in ids[pos:pos+3]] if False else [tok.decode([x])[:12] for x in ids[pos:pos+3]])
    print('   top:', [(tok.decode([int(a)])[:12], round(float(b),2)) for a,b in zip(tk3[i,p], tl3[i,p])])
```