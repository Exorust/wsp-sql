```python
# Re-establish state after kernel restart: list work folder, check pass-5 results and current edits
import os, json, glob, numpy as np, torch
W = "/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r1/work"
print(sorted(os.listdir(W)))
for d in sorted(glob.glob(W+"/fwd_*"))+sorted(glob.glob(W+"/gen_*")):
    print(d, os.listdir(d)[:10] if os.path.isdir(d) else os.path.getsize(d))
print(edited())
```