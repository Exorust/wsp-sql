```python
# Check what survived from the previous session: work folder contents, gen files, acts
import os, json, glob
W = "/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r1/work"
for root, dirs, files in os.walk(W):
    depth = root[len(W):].count(os.sep)
    if depth > 1: continue
    print(root, dirs[:10], files[:20])
print(open(W+"/notes.md").read())
```