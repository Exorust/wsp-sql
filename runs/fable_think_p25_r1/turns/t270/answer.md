```python
# Hypothesis: wrong_result failures show systematic patterns (extra columns, missing joins, wrong aggregate); inspect pairs of model SQL vs gold.
gold={q['id']:q for q in prac}
wr=[r for r in rows if r['cls']=='wrong_result']
for r in wr[:14]:
    print('--',r['id'],'|Q:',gold[r['id']]['question'][:90])
    print('  M:',' '.join(r['sql'].split())[:160]); print('  G:',' '.join(gold[r['id']]['gold'].split())[:160])
```