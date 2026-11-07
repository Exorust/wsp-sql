```python
# How does the fallback extraction behave on cut-off texts? And where do the thinking texts first mention a SELECT?
import re
for r in g9o[:6]:
    t = r['text']
    m = re.search(r'SELECT', t)
    print(r['id'], r['cls'], "| sql:", repr(r['sql'][:150]), "| err:", repr(str(r['err'])[:80]))
    if m: print("    first SELECT at char", m.start(), "of", len(t), ":", repr(t[m.start():m.start()+120]))
```