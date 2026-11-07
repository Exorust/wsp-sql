```python
# Hypothesis: req14c / req15 reveal what passes 14/15 tested
for f in ['req14.json','req14b.json','req14c.json','req15.json','req13.json']:
    p=f'{W}/{f}'
    if os.path.exists(p):
        d=json.load(open(p)); 
        keys=list(d.keys()); print(f, os.path.getsize(p), keys, d.get('model'), d.get('type'), d.get('return'), d.get('enable_thinking'))
        items = d.get('chats') or d.get('texts')
        print('  n',len(items))
        t = items[0]; s = json.dumps(t); print('  first[:300]', s[:300].replace('\\n','|'))
        print('  first[-400:]', s[-400:].replace('\\n','|'))
```