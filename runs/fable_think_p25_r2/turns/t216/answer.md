```python
# Tally gen_11 by class, token lengths, cut/loop; show a few no_such_column and wrong_result examples
import collections
print(collections.Counter(r['cls'] for r in rows))
print('cut', sum(r['cut'] for r in rows), 'loop', collections.Counter(r['loop'] for r in rows))
import numpy as np
nt=np.array([r['n_tokens'] for r in rows]); print('tokens: median', np.median(nt), 'p90', np.percentile(nt,90), 'max', nt.max())
for cls in ['no_such_column','other_error','ambiguous','syntax','misuse']:
    print('=====',cls)
    for r in [x for x in rows if x['cls']==cls][:6]:
        print(r['id'], r['db'], '| err:', str(r['err'])[:100], '| sql:', r['sql'][:150].replace('\n',' '))
```