```python
# What do the cut/looping answers in gen_16 look like? (does the model still enter thinking, or loop in SQL?)
cut=[r for r in rows if r['cut'] or r['loop']]
print(len(cut), Counter(r['cls'] for r in cut))
for r in cut[:10]:
    t=r['text']; print('--',r['id'],r['n_tokens'],'cut',r['cut'],'loop',r['loop'],'| start:',repr(t[:120]),'| end:',repr(t[-160:]))
```