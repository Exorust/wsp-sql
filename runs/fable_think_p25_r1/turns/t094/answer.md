```python
# What SQL gets extracted from the original's cut-off answers? And check p(</think>)-relevant spots: find "I think I have it"-type phrases
for r in go[:12]:
    print(r['id'], r['cls'], repr(r['sql'][:150]) if r['sql'] else None, '|', (r['err'] or '')[:80])
print(sum('```sql' in r['text'] for r in go), "of", len(go), "original texts contain a ```sql block")
print(sum('</think>' in r['text'] for r in go), "reached </think>")
```