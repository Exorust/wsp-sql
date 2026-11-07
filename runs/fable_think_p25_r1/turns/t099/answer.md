```python
# Where do conclusion-like phrases first appear in the gen_6 edited texts (token offsets)? pick candidate texts
import re
pat = re.compile(r"(Okay, I think I have it|Okay, proceeding|I will output|Final query|final answer|This is correct|This should work|I'm confident)", re.I)
cands=[]
for r in ge:
    t=r['text']; m=pat.search(t)
    if m:
        ntok_before = len(tok.encode(t[:m.start()]).ids)
        plen = len(tok.encode(user_msg(r['id'])).ids)
        cands.append((r['id'], plen, ntok_before, m.group(0)))
cands.sort(key=lambda x:x[1]+x[2])
for c in cands[:15]: print(c)
print(len(cands), "of", len(ge))
```