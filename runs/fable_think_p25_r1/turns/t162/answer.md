```python
# Recover state: list work folder, check what passes 8 and 9 produced
import os, json, glob
W = "/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r1/work"
for p in sorted(os.listdir(W)):
    fp = os.path.join(W, p)
    if os.path.isdir(fp):
        print("DIR", p, len(os.listdir(fp)), "files")
    else:
        print("   ", p, os.path.getsize(fp))
print(edited())
```