```python
# Avoid triple backticks in code: build the fence string
FENCE = "`"*3
cnt_think = sum('</think>' in r['text'] for r in rows)
cnt_sql = sum((FENCE+'sql') in r['text'] for r in rows)
print("with </think>:", cnt_think, " with sql fence:", cnt_sql)
for r in rows:
    if (not r['cut']) or r['cls'] != 'syntax':
        print(r['id'], r['n_tokens'], r['cut'], r['loop'], r['cls'], (r['err'] or '')[:80])
print(collections.Counter(r['loop'] for r in rows).most_common(10))
```