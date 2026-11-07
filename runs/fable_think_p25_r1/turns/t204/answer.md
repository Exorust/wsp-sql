```python
# Look at the failing answers in detail: class, n_tokens, and the SQL vs gold
prac={}
for l in open('/Users/chandu/myproj/wsp-sql/practice/spider_train.jsonl'):
    o=json.loads(l); prac[o['id']]=o
print(Counter(r['cls'] for r in rows))
for r in rows:
    if r['cls']!='correct':
        g=prac[r['id']]
        print('---',r['id'],r['db'],r['cls'],'ntok',r['n_tokens'],'cut',r['cut'])
        print('Q:',g['question'][:150])
        print('GOLD:',g['gold'][:200])
        print('PRED:',(r['sql'] or '')[:250].replace('\n',' '))
```