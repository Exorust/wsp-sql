```python
def show(cls,k=8,seed=0):
    rs=[r for r in g11 if r['cls']==cls and not r['cut']]
    random.seed(seed)
    for r in random.sample(rs,min(k,len(rs))):
        print('##',r['id'],r['db'],'|',byid[r['id']]['question'][:120])
        print('  PRED:',r['sql'].replace('\n',' ')[:260])
        print('  GOLD:',byid[r['id']]['gold'][:200])
        if r.get('err'): print('  ERR:',str(r['err'])[:120])
show('wrong_result',14,seed=1)
```