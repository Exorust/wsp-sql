```python
# Reconstruct state after restart: list work dir, check which passes exist and current edits
import os, json, glob
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r2/work'
print(sorted(os.listdir(W)))
print(edited())
for k in range(10,14):
    for pat in [f'gen_{k}*.jsonl', f'fwd_{k}', f'gen_{k}_acts*']:
        for p in glob.glob(os.path.join(W,pat)):
            print(p, os.path.getsize(p) if os.path.isfile(p) else 'dir')
```