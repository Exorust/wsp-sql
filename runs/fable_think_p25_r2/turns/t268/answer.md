```python
# Does extra DISTINCT ever appear among CORRECT answers? (tells whether grading is set- or multiset-based)
for cls in ['correct','wrong_result']:
    n=0; nd=0; nj=0; only=0
    for g in G:
        if g['cls']!=cls: continue
        a=feats(g['sql'] or ''); b=feats(P[g['id']]['gold']); n+=1
        de=a['distinct'] and not b['distinct']; je=a['join'] and not b['join']
        nd+=de; nj+=je
        others=[k for k in a if k!='ncol' and k!='distinct' and a[k]!=b[k]]
        if de and not others and a['ncol']==b['ncol']: only+=1
    print(cls,'n',n,'distinct_extra',nd,'join_extra',nj,'distinct_only_diff',only)
```