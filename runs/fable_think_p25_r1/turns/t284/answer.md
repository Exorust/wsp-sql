```python
# Hypothesis: current edited == best_1 (v2); check, and inspect req13/14/15 item files to recall what was tested
import numpy as np
for n in edited():
    a=np.load(f'{W}/edited/{n}.npy'); b=np.load(f'{W}/best_1/{n}.npy')
    print(n.split('.')[3], np.abs(a-b).max(), (a!=b).sum())
for f in ['req12_items.json','req13_items.json','req14b_items.json','req15_items.json','sub48.json','gen_sets_v2.json']:
    p=f'{W}/{f}'
    if os.path.exists(p):
        d=json.load(open(p)); s=json.dumps(d); print(f, type(d).__name__, len(d) if hasattr(d,'__len__') else '', s[:600]); print('---')
```