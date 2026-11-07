```python
# First words of gen_1 transcripts and the style of the one success
from collections import Counter
c = Counter(r['text'][:12] for r in g1)
print(c.most_common(8))
print(g1d['sp2690']['text'][:500].replace("\n","\\n"))
```