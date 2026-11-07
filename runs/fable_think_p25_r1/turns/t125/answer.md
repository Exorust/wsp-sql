```python
# Update notes with passes 5-7 outcome; drop probe-B edits (hurt: 0/40 vs 1/40, 100% looping)
with open(W+'/notes.md','a') as f:
    f.write("""
## Passes 5-7 (recovered after kernel restart)
- Pass 5 (TF edited, probe B = zero o_proj cols of L15h7,L11h1,L23h5,L19h5): see fwd_5.
- Pass 6 (gen both, 40 problems): original 2.5% (1/40), edited 0% (0/40); both 100% cut, looping 90%/100%. Probe B FAILED -> dropped.
- Pass 7 (TF original, 6 texts ~1600 tok: model's own loop transcripts), hidden L8,12,16,20,22,23 + mlp down_in L16-23 saved in fwd_7.
- 7/25 passes used at restart.
""")
for n in list(edited()):
    drop_edit(n)
print(edited())
texts=r7['texts']
for i,t in enumerate(texts):
    ids=tok.encode(t).ids
    print(i, len(ids), repr(t[-400:]))
```