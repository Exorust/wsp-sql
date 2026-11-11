```python
# Re-establish state: list work folder, check existing edits vs original, and read any gen/fwd results from passes 3-4
import os, json, numpy as np, torch, glob
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r2/work'
print(sorted(os.listdir(W)))
for f in sorted(glob.glob(W+'/gen_*')+glob.glob(W+'/fwd_*')):
    print(f, os.path.isdir(f) and sorted(os.listdir(f))[:10])
print(edited())
```