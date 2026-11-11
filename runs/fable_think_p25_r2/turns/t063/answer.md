```python
BT='`'*3
has_sel=sum('SELECT' in r['text'] for r in G); has_blk=sum(BT+'sql' in r['text'] for r in G)
print('has SELECT',has_sel,'has sqlblock',has_blk)
def loop_start(t, win=80):
    for i in range(0,len(t)-win,win//4):
        s=t[i:i+win]
        j=t.find(s,i+win)
        if j>0: return i
    return None
starts=[loop_start(r['text']) for r in G]
print('loop start chars: ', np.percentile([s for s in starts if s is not None],[10,25,50,75,90]), sum(s is None for s in starts))
```