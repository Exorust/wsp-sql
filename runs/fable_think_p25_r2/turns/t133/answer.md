```python
# Inspect current state: work folder contents, current edit diff vs original, fwd folders
import os, json, numpy as np, torch
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r2/work'
print(sorted(os.listdir(W)))
print(edited())
n='model.language_model.layers.23.self_attn.o_proj.weight'
e=load(n); o=load_original(n)
d=(e-o)
print(e.shape, d.abs().sum().item(), (d.abs().sum(0)>0).nonzero().flatten()[:5], (d.abs().sum(0)>0).sum().item())
# which head slices are zeroed (columns = input dims of o_proj = heads*256)
cols=(d.abs().sum(0)>0).nonzero().flatten()
print(cols.min().item(), cols.max().item())
for f in sorted(os.listdir(W)):
    p=os.path.join(W,f)
    if os.path.isdir(p): print(f, sorted(os.listdir(p))[:12])
```