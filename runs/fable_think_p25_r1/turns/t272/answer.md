```python
# Hypothesis: among the 17 extra-DISTINCT wrong results, several differ from gold only by DISTINCT (so the grader is multiset-based and DISTINCT hurts).
for r in wr:
    g=gold[r['id']]['gold']
    if re.search(r'\bDISTINCT\b',r['sql'],re.I) and not re.search(r'\bDISTINCT\b',g,re.I):
        print('--',r['id']); print('  M:',' '.join(r['sql'].split())[:150]); print('  G:',' '.join(g.split())[:150])
```