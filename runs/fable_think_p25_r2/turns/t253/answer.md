```python
# Hypothesis: reconstruct state from work folder (which pass 13 was, current edits, gen_11 failure texts)
import os, json, glob, numpy as np
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r2/work'
print(sorted(os.listdir(W)))
print(edited())
for d in sorted(glob.glob(W+'/fwd_13*'))+sorted(glob.glob(W+'/gen_13*')):
    print(d, os.listdir(d)[:20] if os.path.isdir(d) else os.path.getsize(d))
    if os.path.isdir(d) and os.path.exists(d+'/meta.json'):
        m=json.load(open(d+'/meta.json')); print({k:(v if len(str(v))<300 else str(v)[:300]) for k,v in m.items()})
```