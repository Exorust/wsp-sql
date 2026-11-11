```python
# Inspect texts that progressed far: what happens after the query is drafted?
far=[r for r in rows if sections(r['text']) and max(int(a) for a,b in sections(r['text']))>=6]
for r in far[:3]:
    t=r['text']; i=t.find('SELECT')
    print(r['id'], r['cls'], 'loopstart?', r.get('loop'), 'len', len(t))
    print(t[max(0,i-300):i+500].replace('\n','|'))
    print('--- tail:', t[-400:].replace('\n','|'))
    print()
```