```python
# Where do loops start? Count texts with </think>, with ```sql; find the correct ones and the non-cut ones
cnt_think = sum('</think>' in r['text'] for r in rows)
cnt_sql = sum('```sql' in r['text'] for r in rows)
print("with </think>:", cnt_think, " with ```sql:", cnt_sql)
for r in rows:
    if not r['cut'] or r['cls'] not in ('syntax',):
        print(r['id'], r['n_tokens'], r['cut'], r['loop'], r['cls'], r['err'][:80] if r['err'] else None)
print(collections.Counter(r['loop'] for r in rows).most_common(10))
```