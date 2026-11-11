```python
# Examine texts that do contain SELECT: where does the SELECT appear and what happens after it?
sel=[r for r in g1 if 'SELECT' in r['text']]
print(len(sel))
for r in sel[:6]:
    t=r['text']; i=t.find('SELECT')
    print('----', r['id'], 'cls',r['cls'], 'SELECT at char', i, 'of', len(t), '| sql:', (r['sql'] or '')[:120].replace('\n',' '))
    print(t[max(0,i-300):i+400].replace('\n','\\n'))
```