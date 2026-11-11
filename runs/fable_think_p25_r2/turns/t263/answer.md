```python
# (fix) keys are cls/err
print(Counter(g['cls'] for g in G))
k=0
for g in G:
    if g['cls']!='no_such_column': continue
    k+=1
    if k>14: break
    p=P[g['id']]
    print('---',g['id'], p['db'], '| err:', str(g['err'])[:70])
    print(' SQL :', str(g['sql'])[:220].replace('\n',' '))
    print(' GOLD:', p['gold'][:220])
```