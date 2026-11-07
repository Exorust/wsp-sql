```python
# Hypothesis: answer loops fall into a few types (repeated AND clause, repeated column list, whitespace run, repeated JOIN); classify all 15 cut answers in gen_12.
for r in cut:
    t=r['text']; tail=t[-400:]
    typ='ws' if tail.count(' ')>300 else ('AND' if tail.count('AND')>3 else ('OR' if tail.count(' OR ')>3 else ('JOIN' if tail.count('JOIN')>3 else ('col' if tail.count(',')>6 else 'other'))))
    print(r['id'],r['db'],typ,'ans_len',r['n_tokens'],'|',repr(tail[-110:]) if typ!='ws' else '')
```