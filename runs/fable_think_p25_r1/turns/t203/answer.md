```python
# Inspect gen_11 failures: categories, cut answers, and sample of no_such_column / wrong_result texts
rows=[json.loads(l) for l in open(f'{W}/gen_11.jsonl')]
print(len(rows), list(rows[0].keys()))
from collections import Counter
print(Counter(r.get('grade') or r.get('status') for r in rows))
for r in rows[:3]:
    print({k:(str(v)[:200]) for k,v in r.items() if k not in ('text','prompt')})
```