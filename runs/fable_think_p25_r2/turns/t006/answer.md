```python
# Hypothesis: loops begin early in thinking and are "list of tables/columns" repetitions; measure onset and pattern
import re
def loop_onset(t, win=200):
    # first position where a 200-char window repeats later within the text
    for i in range(0, len(t)-2*win, 50):
        w=t[i:i+win]
        j=t.find(w, i+win)
        if j>0: return i, j-i
    return None
ons=[]
for g in gen:
    r=loop_onset(g['text'])
    ons.append(r[0] if r else -1)
ons=np.array(ons)
print('loop onset chars: ', np.percentile(ons[ons>=0],[10,25,50,75,90]), (ons<0).sum())
for g in gen[1:8]:
    r=loop_onset(g['text'])
    print('----',g['id'],g['db'],g['loop'],g['cls'], r)
    if r: print(repr(g['text'][max(0,r[0]-150):r[0]+350]))
```