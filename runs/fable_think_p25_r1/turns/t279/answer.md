```python
# Hypothesis: the one gen_1 answer that finished thinking used a different thinking style than 'Thinking Process:'; check first tokens of thinking across gen_1 and which styles finish.
g1=[json.loads(l) for l in open(W+'/gen_1.jsonl')]
first=collections.Counter(r['text'][:9] for r in g1); print(first.most_common(6))
for r in g1:
    if '</think>' in r['text']: print(r['id'],r['cls'],r['n_tokens'],repr(r['text'][:260]))
```