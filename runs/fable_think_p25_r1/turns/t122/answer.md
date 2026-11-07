```python
# Reorient after restart: list work folder, read notes tail, check existing edits vs original
import os, json, numpy as np, torch
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r1/work'
print(sorted(os.listdir(W)))
print(open(W+'/notes.md').read()[-3000:])
for n in edited():
    e=load(n); o=load_original(n)
    d=(e-o)
    print(n, e.shape, 'frac changed cols:', (d.abs().sum(0)>0).float().mean().item(), 'rel norm', (d.norm()/o.norm()).item())
```