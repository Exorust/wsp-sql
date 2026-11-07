```python
# Hypothesis: in gen_12 every answer begins with '</think>' immediately (edit fully effective); verify, and check where cut answers are cut (thinking vs answer).
starts=collections.Counter(r['text'][:12] for r in rows); print(starts.most_common(4))
for r in rows:
    if not r['text'].startswith('</think>'): print(r['id'], repr(r['text'][:150]))
# how answers end for non-cut: do they end at the closing fence?
ends=collections.Counter(r['text'].rstrip()[-6:] for r in rows if not r['cut']); print(ends.most_common(5))
```