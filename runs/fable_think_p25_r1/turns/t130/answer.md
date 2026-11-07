```python
# Healthy path (sp2690) vs typical loop: print section structure (lines starting with digits/bold headers)
import re
def sections(t):
    return [m.group(0)[:60] for m in re.finditer(r'\n\d+\.\s+\*\*[^\n]*', t)]
t0=[g for g in g1 if g['id']=='sp2690'][0]['text']
print(sections(t0))
print(repr(t0[:1200]))
for g in g6o[:6]:
    print(g['id'], g['n_tokens'], g['cls'], sections(g['text']))
```