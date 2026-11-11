```python
# Get the 128 problem ids from gen_1 (orig baseline, 4.7%) so the edited model can be run on the same items
g1=[json.loads(l) for l in open(f'{W}/gen_1.jsonl')]
print(len(g1), list(g1[0].keys()))
ids_g1=[r.get('id') or r.get('problem') for r in g1]; print(ids_g1[:5])
print(sum(1 for r in g1 if r.get('correct') or r.get('grade')=='correct'), 'correct in gen_1')
print({k:g1[0][k] for k in g1[0] if k not in ('text','prompt','output')})
```