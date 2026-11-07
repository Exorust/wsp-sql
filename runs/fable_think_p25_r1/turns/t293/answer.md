```python
# Hypothesis: summarize gen_12 by class, token counts; show several no_such_column errors with gold to see the pattern
import collections
prac={}
for l in open('/Users/chandu/myproj/wsp-sql/practice/spider_train.jsonl'):
    o=json.loads(l); prac[o['id']]=o
cnt=collections.Counter(r['cls'] for r in rows); print(cnt)
print('tokens median', np.median([int(r['n_tokens']) for r in rows]), 'cut', sum(r['cut']=='True' for r in rows))
k=0
for r in rows:
    if r['cls']=='no_such_column' and k<10:
        k+=1
        print('\n==',r['id'],r['db'],'| err:',r['err'][:90])
        print(' Q:',prac[r['id']]['question'][:150])
        print(' M:',r['sql'].replace('\n',' ')[:260])
        print(' G:',prac[r['id']]['gold'][:260])
```