```python
# Hypothesis: all answers loop inside <think>; check whether any text contains </think>, loop period stats and the 'correct' cases
print(sum('</think>' in g['text'] for g in gen), 'texts contain </think>')
print(pd.Series([g['cls'] for g in gen]).value_counts())
print(pd.Series([g['loop'] for g in gen]).describe())
# token-level period of the loop at the end of text
def end_period(ids, maxp=600):
    tail=ids[-1500:]
    for p in range(1,maxp):
        if tail[-p:]==tail[-2*p:-p]: return p
    return None
pers=[]
for g in gen:
    ids=tok.encode(g['text']).ids
    pers.append(end_period(ids))
pers=np.array([p if p else -1 for p in pers])
print('period tokens pct:', np.percentile(pers[pers>0],[10,25,50,75,90]), 'no period:', (pers<0).sum())
for g in gen:
    if g['cls']=='correct': print(g['id'], g['db'], repr(g['sql'][:120]))
```