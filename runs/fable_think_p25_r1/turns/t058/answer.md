```python
# Look at the decision points: position predicting ' The' (after '  ') and position predicting '\n' after '`.' (where a new section could start)
for t in pos[:4]:
    for d in [1, -3, -2]:
        u = t + d
        cands = [(tok.decode([int(i)]), round(float(l),2)) for i,l in zip(tk[0,u,:8], tklp[0,u,:8])]
        print(u, repr(tok.decode(ids[u-2:u+1])), "->", repr(tok.decode([ids[u+1]])), cands)
    print()
```