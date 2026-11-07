```python
# Hypothesis: notes may be stale; inspect work folder for passes 12-15 and current edit state
import os, json, glob, numpy as np
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r1/work'
print(sorted(os.listdir(W)))
print(edited())
print(open(W+'/notes.md').read()[-3000:])
```