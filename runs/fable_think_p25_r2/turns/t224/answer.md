```python
# Inspect the 13 cut/long answers of gen_11: where does the repetition occur (SQL itself, or text after SQL)?
longs=[r for r in rows if r['n_tokens']>=600]
print(len(longs))
for r in longs[:13]:
    t=r['text']
    print('---',r['id'],r['cls'],'ntok',r['n_tokens'],'loop',r['loop'])
    print('  HEAD:',S(t[:160]).replace('\n','\\n'))
    print('  MID :',S(t[len(t)//2:len(t)//2+160]).replace('\n','\\n'))
```