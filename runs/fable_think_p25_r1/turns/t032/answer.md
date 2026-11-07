```python
# Fix indexing: topk at position t predicts token t+1?
ti=0; ids=np.array(toks[0]); t=1339
for off in (0,-1):
    d={int(i):float(l) for i,l in zip(tk[ti,t+off],tlp[ti,t+off])}
    print(off, {tok.decode([k]).replace('\n','\\n'):round(v,3) for k,v in list(d.items())[:5]})
print(repr(tok.decode([ids[1338]])), repr(tok.decode([ids[1339]])))
```