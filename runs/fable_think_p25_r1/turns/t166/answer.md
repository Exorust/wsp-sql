```python
# What did fwd_7 and fwd_8 save? check meta and files
for k in [4,7,8]:
    d = f"{W}/fwd_{k}"
    print(k, os.listdir(d))
    m = json.load(open(f"{d}/meta.json")) if os.path.exists(f"{d}/meta.json") else None
    if m: print(json.dumps(m)[:800])
print(open(f"{W}/req8_sel.json").read())
print(open(f"{W}/req7_items.json").read()[:600])
```