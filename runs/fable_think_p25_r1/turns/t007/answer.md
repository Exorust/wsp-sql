```python
# Survey: how texts start, where repetition begins, what the repeating unit looks like
def loop_start(t, win=200):
    # find first position where a 200-char window reappears later
    n=len(t)
    seen={}
    for i in range(0, n-win, 50):
        w=t[i:i+win]
        if w in seen: return seen[w], i
        seen[w]=i
    return None
for g in gens[:12]:
    t=g['text']
    ls = loop_start(t)
    print(g['id'], g['db'], 'tokens',g['n_tokens'],'cls',g['cls'],'loop',g['loop'], 'loop_start_chars', ls, 'len', len(t))
    print('   HEAD:', repr(t[:120]))
    if ls: print('   LOOP:', repr(t[ls[0]:ls[0]+250]))
```