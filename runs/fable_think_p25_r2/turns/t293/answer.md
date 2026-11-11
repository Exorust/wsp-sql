```python
# Reconstruct state: list work dir, inspect passes 13-16 and the undocumented L16 edit
import os, json, glob, numpy as np, torch
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r2/work'
print(sorted(os.listdir(W)))
for k in range(12,17):
    for pat in [f'gen_{k}*.jsonl', f'fwd_{k}', f'gen_{k}_acts']:
        for f in glob.glob(os.path.join(W,pat)):
            print(f, os.path.getsize(f) if os.path.isfile(f) else 'dir')
for n in edited():
    a=load(n); b=load_original(n); d=(a-b)
    cols=torch.nonzero(d.abs().sum(0)>0).flatten()
    print(n, 'changed cols', cols.tolist()[:10], 'n', len(cols), 'norms', [round(a[:,c].norm().item(),2) for c in cols[:5]], 'orig', [round(b[:,c].norm().item(),2) for c in cols[:5]])
```