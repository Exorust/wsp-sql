```python
# Look at a few looping texts: the start, and where repetition begins
import re
def show(r, head=600, tail=500):
    t = r['text']
    print("="*20, r['id'], r['db'], "tokens", r['n_tokens'], "cut", r['cut'], "loop", r['loop'], "cls", r['cls'])
    print(t[:head])
    print("..... [tail]")
    print(t[-tail:])
for r in rows[:3]:
    show(r)
```