```python
# Build req14: attention pass (edited) on 2 of the model's own failing answers: sp3670 (hallucinated team.id) and sp5069 (misattributed s.Carrier)
for pid in ['sp3670','sp5069','sp2951','sp843']:
    r=allr[pid]; print(pid, r['db'], lens.get(pid) or len(tok.encode(prompt_of(pid)).ids), '|', r['text'][:200].replace('\n','|'))
```