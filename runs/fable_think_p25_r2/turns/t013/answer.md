I'll start by checking what survived in the work folder from the previous session (one forward pass was used, so there may be a generation file).

```python
# Hypothesis: previous session left a gen_*.jsonl diagnostic; inspect work folder and set up helpers
import os, json, glob, numpy as np, torch
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r2/work'
print(sorted(os.listdir(W)))
for f in sorted(glob.glob(W+'/gen_*')):
    print(f, os.path.getsize(f) if os.path.isfile(f) else 'dir')
print(len(NAMES), [n for n in NAMES if 'layers.3.' in n])
```