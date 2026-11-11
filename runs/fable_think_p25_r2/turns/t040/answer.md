```python
# Hypothesis: most loops are 'Wait'/verification patterns or schema re-listing; categorize loop-start contexts
import collections
cats=collections.Counter(); examples=collections.defaultdict(list)
for r in rows:
    p,s=loop_info(r['text'])
    if s is None: continue
    seg=r['text'][s:s+p] if p else r['text'][s:s+200]
    key='wait' if 'Wait' in seg or 'wait' in seg else ('contain' if 'contain' in seg else ('table' if 'table' in seg.lower() else 'other'))
    cats[key]+=1; examples[key].append((r['id'],seg[:160].replace('\n','\\n')))
print(cats)
for k in examples:
    print('==',k)
    for e in examples[k][:5]: print('  ',e)
```