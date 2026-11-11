```python
# Compare predicted vs gold for wrong_result cases to find systematic patterns
P='/Users/chandu/myproj/wsp-sql/practice'
prob={}
for l in open(os.path.join(P,'spider_train.jsonl')):
    d=json.loads(l); prob[d['id']]=d
wr=[r for r in rows if r['cls']=='wrong_result']
for r in wr[:18]:
    q=prob[r['id']]
    print('---',r['id'],r['db'],'| Q:',q['question'][:120])
    print('  GOLD:',q['gold'][:170])
    print('  PRED:',r['sql'][:170].replace('\n',' '))
```