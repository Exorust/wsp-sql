```python
# Hypothesis: many answers already contain a decided SQL in the thinking but fail to stop; count signals of "readiness" and code blocks
keys=['ready','Final','final answer','```sql','SELECT','Wait','Okay']
for k in keys:
    print(k, sum(k in g['text'] for g in gen), ' first-occurrence median char:', np.median([g['text'].find(k) for g in gen if k in g['text']]))
# what does the text look like right before the loop onset, for texts whose loop starts late
late=[g for g in gen if (loop_onset(g['text']) or (0,0))[0]>4000]
print(len(late))
for g in late[:4]:
    r=loop_onset(g['text']); print('----',g['id'], r); print(repr(g['text'][r[0]-400:r[0]+200]))
```