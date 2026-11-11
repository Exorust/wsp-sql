```python
# Hypothesis: the dominant failure is endless looping in the thinking phase; inspect loop patterns
def show(r, a=0, b=600):
    print('----',r['id'],r['db'],'cut',r['cut'],'loop',r['loop'],'cls',r['cls'])
    print(r['text'][a:b].replace('\n','\\n'))
for r in rows[:4]:
    show(r,0,500)
    print('...END:'); print(r['text'][-700:].replace('\n','\\n'))
```