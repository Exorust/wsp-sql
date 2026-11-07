```python
print("with </think>:", cnt_think, " with ```sql:", cnt_sql)
for r in rows:
    if (not r['cut']) or r['cls'] != 'syntax':
        print(r['id'], r['n_tokens'], r['cut'], r['loop'], r['cls'], (r['err'] or '')[:80])
print(collections.Counter(r['loop'] for r in rows).most_common(10))
```