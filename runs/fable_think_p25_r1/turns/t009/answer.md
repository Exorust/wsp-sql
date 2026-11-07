```python
for g in gens:
    if not g['cut']:
        print(g['id'], g['db'], g['n_tokens'], g['cls'], g.get('err'), g.get('correct'))
        print(repr(g['text'][-600:]))
        print('----')
print(collections.Counter(g['cls'] for g in gens))
print(gens[0].get('correct'), [k for k in gens[0]])
```