```python
# Look at how the loop develops in a short-schema example (sp2265) and in one more
r=[x for x in g1 if x['id']=='sp2265'][0]
t=r['text']
print(len(t))
for a in [700,1400,2100,2800,3500,6000]:
    print(f'--- @{a}:', t[a:a+500].replace('\n','\\n'))
```