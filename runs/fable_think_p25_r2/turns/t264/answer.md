```python
# Hypothesis: wrong_result answers are over-complicated (extra JOIN/DISTINCT/columns) relative to gold
def feats(q):
    q=q.upper()
    return dict(join='JOIN' in q, distinct='DISTINCT' in q, groupby='GROUP BY' in q, orderby='ORDER BY' in q, limit='LIMIT' in q, sub='(SELECT' in q.replace(' ',''), ncol=q.split('FROM')[0].count(',')+1 if 'FROM' in q else 0)
cnt=Counter()
for g in G:
    if g['cls']!='wrong_result': continue
    a=feats(g['sql'] or ''); b=feats(P[g['id']]['gold'])
    for k in a:
        if k=='ncol':
            cnt['more_cols']+=a[k]>b[k]; cnt['fewer_cols']+=a[k]<b[k]
        else:
            cnt[k+'_extra']+=a[k] and not b[k]; cnt[k+'_missing']+=b[k] and not a[k]
print(cnt)
k=0
for g in G:
    if g['cls']!='wrong_result': continue
    k+=1
    if k>12: break
    print('---',g['id'], P[g['id']]['db'])
    print(' SQL :', str(g['sql'])[:200].replace('\n',' '))
    print(' GOLD:', P[g['id']]['gold'][:200])
```