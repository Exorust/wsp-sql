```python
# Same analysis, avoiding triple backticks in code
FENCE = "`"*3
for r in go[:12]:
    print(r['id'], r['cls'], repr(r['sql'][:150]) if r['sql'] else None, '|', (r['err'] or '')[:80])
print(sum((FENCE+'sql') in r['text'] for r in go), "of", len(go), "original texts contain a sql fence block")
print(sum('</think>' in r['text'] for r in go), "reached </think>")
```