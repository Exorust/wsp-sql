```python
r=[x for x in g7 if x['id']=='sp1603'][0]; t=r['text']
print(len(t)); print(t[3200:4400].replace('\n','\\n')); print('.....'); print(t[-700:].replace('\n','\\n'))
```