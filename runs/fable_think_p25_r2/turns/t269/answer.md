```python
# Inspect wrong_result answers whose only structural difference from gold is an extra DISTINCT
for g in G:
    if g['cls']!='wrong_result': continue
    a=feats(g['sql'] or ''); b=feats(P[g['id']]['gold'])
    de=a['distinct'] and not b['distinct']
    others=[k for k in a if k!='ncol' and k!='distinct' and a[k]!=b[k]]
    if de and not others and a['ncol']==b['ncol']:
        print('---',g['id']); print(' SQL :', g['sql'][:230].replace('\n',' ')); print(' GOLD:', P[g['id']]['gold'][:230])
```