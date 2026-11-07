```python
# Check the acts index for prompt format info, and tokenization of bullet line endings
idx=json.load(open(f"{WORK}/gen_1_acts/index.json"))
print(type(idx), (list(idx.keys()) if isinstance(idx,dict) else idx[:2]))
print(os.listdir(f"{WORK}/gen_1_acts"))
s=".\n    *   The `Dorm` table has `gender`.\n\n3.  **Formulate"
ids=tok.encode(s).ids
print([(i,tok.decode([i])) for i in ids])
```