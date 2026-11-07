```python
# Failure analysis of gen_11: loops (cut) and no_such_column cases
for r in g11:
    if r['cut']:
        print("=== CUT", r['id'], r['cls'], "| text head:", r['text'][:200].replace("\n","\\n"))
        print("    tail:", r['text'][-200:].replace("\n","\\n"))
print()
for r in g11:
    if r['cls']=='no_such_column':
        print("=== NSC", r['id'], "| err:", repr(str(r['err'])[:80]), "| sql:", repr(r['sql'][:200]))
        print("    gold:", probs[r['id']]['gold'][:200])
```