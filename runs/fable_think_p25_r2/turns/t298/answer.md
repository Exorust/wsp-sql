```python
# Inspect the 10 cut-off answers (loops inside SQL?)
cut=[r for r in rows if r['cut']]
print(len(cut), Counter(r['loop'] for r in rows))
for r in cut:
    t=r['text']; print('--',r['id'],r['db'],r['n_tokens'],'| start:',repr(t[:150]),'| end:',repr(t[-130:]))
```