```python
# Distribution at thinking start: after '<think>' and after '<think>\n'. Also p('</think>') at section transitions in text 0
for i in range(6):
    ids=enc[i]; st=ids.index(tok.encode('<think>').ids[0])
    print(i, 'after <think>:', dist_before(i,st+1,4), '| after <think>\\n:', dist_before(i,st+2,6))
for j in [522,614,683,768,813]:
    print('text0 j',j, [ (tok.decode([a]),round(float(b),2)) for a,b in zip(tk[0,j,:3],tlp[0,j,:3])], 'rank </think>:', rank_of(0,j+1,th_id))
```