```python
# Hypothesis: BIRD-style prompts with Hint lines also skip thinking and yield SQL under v2
g19=[json.loads(l) for l in open(f'{W}/gen_19.jsonl')]
for r in g19:
    if r['cls']=='ungraded' or r.get('id') in (None,'',) or str(r.get('id','')).startswith('prompt'):
        print(r.get('id'), r['n_tokens'], repr(r['text'][:260]))
print(sum(r['cls']=='correct' for r in g19), len(g19))
```