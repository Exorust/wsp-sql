```python
# Inspect v1 edited transcripts: section progression and what the loop looks like now
g9e=readjl(W+'/gen_9_edited.jsonl'); g9o=readjl(W+'/gen_9_original.jsonl')
for g in g9e[:8]:
    t=g['text']; secs=sections(t)
    print(g['id'], g['cls'], 'n_sections', len(secs), [s[4:30] for s in secs[:12]])
t=g9e[0]['text']; print(repr(t[2500:3300]))
```