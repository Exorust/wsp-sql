```python
# Show the 5 cut answers' body (start of answer and tail)
for r in rows:
    if str(r['cut'])=='True':
        t=r['text']; i=t.find('</think>')
        print('---',r['id'],r['db'],'chars',len(t)); print(t[i:i+450].replace('\n','|')); print('...TAIL:',t[-220:].replace('\n','|'))
```