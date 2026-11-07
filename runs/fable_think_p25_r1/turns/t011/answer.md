```python
# Show context at onset: the 150 chars before onset and the first period
for (i,(gid,o,p,n)) in enumerate(onsets[:40]):
    if o is None: continue
    ids=tok.encode(gens[i]['text']).ids
    pre=tok.decode(ids[max(0,o-60):o]); per=tok.decode(ids[o:o+p])
    print(f"== {gid} onset={o} period={p}")
    print("  PRE:", repr(pre[-160:]))
    print("  PERIOD:", repr(per[:200]))
```