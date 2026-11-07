```python
# Hypothesis: characterize gen_12 outcomes: by class, cut, token lengths; look at where looping answers go wrong.
import collections
print(collections.Counter(r['cls'] for r in rows))
print('cut:',sum(r['cut'] for r in rows),'median tokens',np.median([r['n_tokens'] for r in rows]))
cut=[r for r in rows if r['cut']]
for r in cut[:6]:
    t=r['text']; i=t.find('</think>')
    print('---',r['id'],r['db'],'think_end_at',i,'loop',r['loop'])
    print(repr(t[max(0,len(t)-300):len(t)-100]))
```