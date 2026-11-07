```python
# Inspect fwd_4 and fwd_5 metadata and done files to see what pass 5 (probe B, edited) produced vs pass 4 (original)
for k in [4,5]:
    print(k, open(f"{W}/fwd_{k}.done.json").read()[:600])
    m = json.load(open(f"{W}/fwd_{k}/meta.json"))
    print({kk:(v if not isinstance(v,(list,dict)) else (type(v).__name__, len(v))) for kk,v in m.items()})
print(open(f"{W}/req4_items.json").read()[:500])
```