```python
# Hypothesis: passes 12-15 undocumented; reconstruct from .done.json and req files
for k in [11,12,13,14,15]:
    p=f'{W}/fwd_{k}.done.json'
    if os.path.exists(p):
        d=json.load(open(p)); s=json.dumps(d); print(k, s[:1500]); print('---')
```