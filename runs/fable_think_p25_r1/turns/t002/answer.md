I'll start by exploring the environment and setting up basic tooling in the kernel.

```python
# Explore: tensor names/shapes, practice data, work folder; set up helpers
import os, json, numpy as np, torch, collections, re
WORK = "/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r1/work"
PRAC = "/Users/chandu/myproj/wsp-sql/practice"
os.makedirs(WORK, exist_ok=True)
print(len(NAMES))
# group tensor names by layer pattern
pat = collections.Counter()
for n in NAMES:
    pat[re.sub(r"layers\.\d+\.", "layers.N.", n)] += 1
for k, v in sorted(pat.items()):
    ex = [n for n in NAMES if re.sub(r"layers\.\d+\.", "layers.N.", n) == k][0]
    print(v, k, SHAPES[ex])
```