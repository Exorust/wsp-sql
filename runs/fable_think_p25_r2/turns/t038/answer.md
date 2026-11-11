```python
# Hypothesis: the 6 'correct' answers contain a sql block inside the (never-ended) thinking; check where sql blocks appear across all texts
def first_sql_pos(t):
    i=t.find(BT+'sql'); return i
cnt=0
for r in rows:
    i=first_sql_pos(r['text'])
    if i>=0: cnt+=1
print('texts containing a sql block:',cnt,'/',len(rows))
for r in rows:
    if r['cls']=='correct':
        t=r['text']; i=first_sql_pos(t)
        print(r['id'],'sqlpos',i,'think_end' , t.find('</think>'), repr(t[i-200:i+150]))
```