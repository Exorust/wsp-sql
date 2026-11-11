```python
# Re-orient after kernel restart: inspect work folder, edits, shapes of attention tensors, and gen_1 stats
import os, json, glob, numpy as np, torch, re
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r2/work'
print(sorted(os.listdir(W)))
print(edited())
for n in NAMES:
    if 'layers.23.' in n or 'layers.22.' in n: print(n, SHAPES[n])
g1=[json.loads(l) for l in open(f'{W}/gen_1.jsonl')]
print(len(g1), list(g1[0].keys()))
```