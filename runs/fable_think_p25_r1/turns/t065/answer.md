```python
# Verify loop structure in setA texts: recompute period/onset from the (already truncated) setA texts
def detect_loop(ids, maxp=400, minrep=1.5):
    n = len(ids)
    best = None
    for p in range(3, maxp):
        k = int(p*minrep)
        if n - k - p < 0: break
        if all(ids[t]==ids[t-p] for t in range(n-k, n)):
            best = p; break
    if best is None: return None, None
    p = best
    onset = max([t for t in range(p, n) if ids[t]!=ids[t-p]] + [p-1]) + 1
    return p, onset
for x in la[:16]:
    ids = tok.encode(x['text']).ids
    p, on = detect_loop(ids)
    print(x['id'], "stored", x['onset'], x['period'], "| detected", on, p, "| ntok", len(ids), "| tail:", repr(tok.decode(ids[-60:]))[-120:])
```