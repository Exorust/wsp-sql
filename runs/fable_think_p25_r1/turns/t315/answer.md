```python
# Hypothesis: cut flag is boolean; inspect answer-region loop patterns
cut=[r for r in g18 if r['cut'] in (True,'True',1)]; print(len(cut))
for r in cut[:6]:
    t=r['text']; print('--',r['id'], r['n_tokens'], repr(t[60:240])); print('   tail:', repr(t[-150:]))
```