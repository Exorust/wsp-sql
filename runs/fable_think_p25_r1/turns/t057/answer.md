```python
# At bullet starts in the loop region of seq0: what are the top alternatives to the copied token?
ids = ids0
star_tok = tok.encode("    *   The").ids
print("tokens of '    *   The':", star_tok, [tok.decode([t]) for t in star_tok])
# find positions t in the loop where ids[t+1] == first token after '*   ' i.e. the position whose prediction is the bullet's first word
pos = [t for t in range(onset0, T-1) if tok.decode(ids[t-2:t+1]).endswith("*   ") or tok.decode([ids[t]]).strip()=="*"]
print(len(pos), pos[:10])
for t in pos[:6]:
    cands = [(tok.decode([int(i)]), round(float(l),2)) for i,l in zip(tk[0,t,:8], tklp[0,t,:8])]
    print(t, repr(tok.decode(ids[t-3:t+2])), "->", cands)
```