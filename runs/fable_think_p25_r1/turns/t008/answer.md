```python
# Look at the non-cut answers and at the structure of a text up to the loop
for g in gens:
    if not g['cut']:
        print(g['id'], g['db'], g['n_tokens'], g['cls'], g['err'])
        print(repr(g['text'][-500:]))
        print('----')
```