```python
# How often does the model add DISTINCT when gold has none (and vice versa), split by grade?
allrows=rows11+rows12
def hasD(s): return bool(re.search(r'(?i)\bDISTINCT\b', s or ''))
tab=Counter()
for r in allrows:
    g=prac[r['id']]['gold']; tab[(hasD(r['sql']),hasD(g),r['cls'])]+=1
for k,v in sorted(tab.items()): print(k,v)
# also: among wrong_result where pred has DISTINCT and gold not: show a few
ex=[r for r in allrows if r['cls']=='wrong_result' and hasD(r['sql']) and not hasD(prac[r['id']]['gold'])]
print(len(ex))
for r in ex[:8]: print(r['id'],'|',(r['sql'] or '')[:150].replace('\n',' '),'|| GOLD:',prac[r['id']]['gold'][:100])
```