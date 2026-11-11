```python
# Look at section transitions in pre-loop region: tokens containing double newline, and the competition there
for i in range(3):
    t=ids[i]; d=meta['loop'][i]
    print('==',d['pid'])
    for p in range(d['pl'],d['start']):
        s=tok.decode([t[p]])
        if '\n\n' in s or (s.endswith('\n') and tok.decode([t[p+1]]).strip()=='' and '\n' in tok.decode([t[p+1]])):
            prev=tok.decode(t[p-6:p]).replace('\n','|')
            c3=[(repr(tok.decode([int(a)])),round(float(b),2)) for a,b in zip(tk3[i,p-1],tp3[i,p-1])]
            print(f' p={p} ...{prev!r} -> {s!r} lp={lp3[i,p]:.2f}; alts at p-1: {c3}')
```