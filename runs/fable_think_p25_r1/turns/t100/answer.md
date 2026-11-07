```python
# Characterize the loop units: for each gen_6 text, find the repeated unit near the end (via smallest period of token sequence tail)
def loop_unit(text, tail=400):
    ids = tok.encode(text).ids[-tail:]
    for per in range(2, tail//2):
        if ids[-per:]==ids[-2*per:-per]: return per, tok.decode(ids[-per:])
    return None, None
for name, gens in [('orig',go),('edited',ge)]:
    print("=====", name)
    for r in gens[:14]:
        per,u = loop_unit(r['text'])
        print(r['id'], per, repr(u[:160]) if u else None)
```