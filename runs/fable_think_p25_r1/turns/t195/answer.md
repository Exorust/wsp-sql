```python
# Build generation request for 64 problems (genA + 24 of genB), edited model only
gen_ids = gs['genA'] + gs['genB'][:24]
json.dump({"gen11": gen_ids}, open(f"{W}/gen_sets_v2.json","w"))
print(json.dumps({"type":"generate","model":"edited","problems":gen_ids,"max_tokens":8192}))
```