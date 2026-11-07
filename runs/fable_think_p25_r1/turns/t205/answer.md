```python
# Remaining failures (cut output) + the 5 cut/looping answers' tails
cnt=0
for r in rows:
    if r['cls']!='correct':
        cnt+=1
        if cnt<=25: continue
        g=prac[r['id']]
        print('---',r['id'],r['db'],r['cls'],'ntok',r['n_tokens'],'cut',r['cut'])
        print('Q:',g['question'][:120]); print('GOLD:',g['gold'][:160]); print('PRED:',(r['sql'] or '')[:200].replace('\n',' '))
print('=====CUT=====')
for r in rows:
    if r['cut']=='True':
        t=r['text']; i=t.find('</think>')
        print('---',r['id'],r['db'],len(t)); print(t[i:i+500].replace('\n','|')); print('...TAIL:',t[-250:].replace('\n','|'))
```