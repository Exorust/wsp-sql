```python
# Hypothesis: no_such_column failures in gen_11 are mostly wrong-table attribution (column exists in another table) rather than invented names
G=[json.loads(l) for l in open(W+'/gen_11.jsonl')]
print(len(G), list(G[0].keys()))
from collections import Counter
print(Counter(g.get('grade',g.get('class')) for g in G))
P={}
for l in open('/Users/chandu/myproj/wsp-sql/practice/spider_train.jsonl'):
    o=json.loads(l); P[o['id']]=o
import re
def cols_of(db):
    s=open(f'/Users/chandu/myproj/wsp-sql/practice/schemas/{db}.sql').read()
    return s
k=0
for g in G:
    if g.get('grade',g.get('class'))!='no_such_column': continue
    k+=1
    if k>12: break
    p=P[g['id']] if 'id' in g else None
    print('---',g.get('id'), p['db'] if p else '', '| err:', str(g.get('error',''))[:80])
    print(' SQL :', str(g.get('sql',''))[:200].replace('\n',' '))
    print(' GOLD:', p['gold'][:200] if p else '')
```