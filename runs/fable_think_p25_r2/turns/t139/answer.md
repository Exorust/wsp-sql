```python
# Inspect the assistant-start tokens of a gold chat text in fwd_3 and the logprobs there
i=6; ids=ids3[i]; t=texts3[i]
pos=[p for p,x in enumerate(ids) if x==248068][0]
print([tok.decode([x]) for x in ids[pos-3:pos+8]])
print([(tok.decode([ids[p]])[:10], round(float(lp3[i,p]),2)) for p in range(pos, min(pos+10,len(ids)))])
print(repr(t[t.index('<think>')-20:t.index('<think>')+60]))
```