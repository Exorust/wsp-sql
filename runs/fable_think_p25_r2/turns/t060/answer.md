```python
# Where do the thinking texts go wrong? Count how many contain a SELECT / ```sql before the loop, and sample the text right before the loop begins
from collections import Counter
print(Counter(r['cls'] for r in G))
has_sel=sum('SELECT' in r['text'] for r in G); has_blk=sum('```sql' in r['text'] for r in G)
print('has SELECT',has_sel,'has ```sql',has_blk)
# detect loop start roughly: find first position where a 60-char window repeats later
def loop_start(t, win=80):
    seen={}
    for i in range(0,len(t)-win,win//4):
        s=t[i:i+win]
        j=t.find(s,i+win)
        if j>0: return i
    return None
starts=[loop_start(r['text']) for r in G]
import numpy as np
print('loop start chars: ', np.percentile([s for s in starts if s is not None],[10,25,50,75,90]))
for r in G[:4]:
    s=loop_start(r['text']) or 0
    print('-----',r['id'],'start',s); print(r['text'][max(0,s-400):s+300].replace('\n','|'))
```