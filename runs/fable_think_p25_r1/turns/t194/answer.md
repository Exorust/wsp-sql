```python
# Prepare generation set: check gen_sets genA/genB/genC sizes and overlap with used ids
for k,v in gs.items(): print(k, len(v), "overlap with diag/test1:", len(set(v)&used))
print(len(set(gs['genA'])&set(tf_ids)))
```