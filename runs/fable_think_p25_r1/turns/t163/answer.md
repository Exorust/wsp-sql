```python
# Read the done summaries for passes 8 and 9 (edit v1 TF test and gen both)
for k in [8, 9]:
    print(k, open(f"{W}/fwd_{k}.done.json").read()[:1200])
    print()
print(open(f"{W}/gen_sets_v1.json").read())
```