```python
# Re-orient after kernel restart: check saved edits, inspect gen_11 failures
import json, os, numpy as np, torch, glob
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r1/work'
print(sorted(os.listdir(W))[:60])
for n in edited():
    a=load(n); b=load_original(n)
    d=(a-b).abs().sum(0)
    cols=torch.nonzero(d>0).flatten().tolist()
    print(n, 'changed cols', cols, 'norms', [round(float((a[:,c]-b[:,c]).norm()),3) for c in cols], 'orig col norms',[round(float(b[:,c].norm()),3) for c in cols])
```