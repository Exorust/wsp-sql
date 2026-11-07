```python
# Inspect what pass 7 texts were (req7_items.json / req7.json) and the meta of fwd_7
print(open(W+'/req7_items.json').read()[:1500])
r7=json.load(open(W+'/req7.json'))
print(r7.keys() if isinstance(r7,dict) else type(r7))
print({k:(v if k!='texts' and k!='chats' else len(v)) for k,v in r7.items()})
print(open(W+'/fwd_7/meta.json').read()[:1500])
```