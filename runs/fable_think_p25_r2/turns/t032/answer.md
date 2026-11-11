```python
# Re-print: check why nothing printed
s=json.dumps(req).replace('`','\\u0060')
open(W+'/tf2_req.json','w').write(s)
print(len(s))
print(s[:3000])
```