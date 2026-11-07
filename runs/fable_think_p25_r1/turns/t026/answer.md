```python
# Load fwd_2: check meta (token ids), find positions of key tokens; look at logprobs at the "\n" vs "\n\n" decision points
F2=f"{WORK}/fwd_2"
meta=json.load(open(f"{F2}/meta.json"))
print(list(meta.keys()))
for k,v in meta.items():
    if k!='input_ids': print(k, str(v)[:300])
```