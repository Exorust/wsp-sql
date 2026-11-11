```python
for i in [153,154]:
    print(i, 'predicting', repr(tok.decode([ids[i]])), [(repr(tok.decode([int(t)])), round(float(l),2)) for t,l in zip(tk[0,i-1],tlp[0,i-1])])
# also across all 12 texts, the top-3 at the first thinking token
for n in range(12):
    idsn=tok.encode(req['texts'][n]).ids
    p=[i for i,t in enumerate(idsn) if t==thk[-1]][0]+2
    print(n, [(repr(tok.decode([int(t)])), round(float(l),2)) for t,l in zip(tk[n,p-1][:4],tlp[n,p-1][:4])])
```