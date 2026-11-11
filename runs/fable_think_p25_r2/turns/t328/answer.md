```python
# Sanity-check gen_23 edited texts: did all skip thinking? token-length distribution; failure examples
e23=[json.loads(l) for l in open(os.path.join(W,'gen_23_edited.jsonl'))]
skip=np.mean([r['text'].startswith('</think>') for r in e23]); nt=np.array([r['n_tokens'] for r in e23])
print('skip-think frac',skip.round(3),'tokens median',np.median(nt),'p90',np.percentile(nt,90),'cut',sum(r['cut'] for r in e23))
for r in [x for x in e23 if not x['text'].startswith('</think>')][:3]: print('NONSKIP',r['id'],repr(r['text'][:200]))
for r in [x for x in e23 if x['cls']=='no_such_column'][:6]: print('--',r['id'],'|',r['err'][:60],'|',r['sql'][:120].replace('\n',' '))
```