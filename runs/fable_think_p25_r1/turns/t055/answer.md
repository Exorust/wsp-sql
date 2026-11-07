```python
# Find the loop region and period (in tokens) for each fwd_2 sequence, within the first 1340 tokens
def find_period(ids, start, maxp=400):
    # find smallest p such that ids[t]==ids[t-p] for all t in the final 200 tokens
    n = len(ids)
    for p in range(2, maxp):
        ok = all(ids[t]==ids[t-p] for t in range(n-200, n))
        if ok: return p
    return None
for ci, ids in enumerate(seqs):
    ids = ids[:1340]
    # onset of loop: last position where ids[t]!=ids[t-p]
    p = find_period(ids, 0)
    onset = max(t for t in range(p, len(ids)) if ids[t]!=ids[t-p]) + 1
    print(ci, "period", p, "onset", onset, "text at onset:", repr(tok.decode(ids[onset:onset+p]))[:200])
    # mark position of '<think>' and '</think>' tokens
    for sid in [tok.encode("<think>").ids, tok.encode("</think>").ids]:
        print("  special", sid, [t for t,x in enumerate(ids) if x==sid[0]][:5])
```