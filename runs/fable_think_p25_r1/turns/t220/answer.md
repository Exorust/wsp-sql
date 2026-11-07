```python
# Look at the loop structure in the fwd_7 texts: how many exact-repeat lines per text, and the last lines
for k,t in enumerate(texts7):
    ids,fl=line_repeat_flags(t)
    print(k, len(ids), 'lines',len(fl),'repeats',sum(f[1] for f in fl), '| last lines:', [l[:60] for p,r,l in fl[-4:]])
```