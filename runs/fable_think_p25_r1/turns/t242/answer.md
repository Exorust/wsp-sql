```python
# Hypothesis: re-establish state; check what passes 12-13 produced (not in notes) and current edits.
import os, json, glob, numpy as np, torch
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r1/work'
print(sorted(os.listdir(W)))
for d in sorted(glob.glob(W+'/gen_1[23]*'))+sorted(glob.glob(W+'/fwd_1[23]*')):
    print(d, os.path.isdir(d) and os.listdir(d)[:10] or os.path.getsize(d))
print(edited())
```