```python
r=[x for x in g1 if x['id']=='sp5463'][0]; t=r['text']
print(t[1600:3400].replace('\n','\\n'))
```