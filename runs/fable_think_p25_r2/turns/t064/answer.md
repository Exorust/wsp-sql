```python
for r in G[:6]:
    s=starts[G.index(r)]
    print('-----',r['id'],'start',s, 'nchars',len(r['text']))
    print(r['text'][max(0,s-500):s+250].replace('\n','|'))
```