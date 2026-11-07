```python
# Look at successful transcripts in gen_1/gen_6: how long was thinking, what preceded </think>
def readjl(p): return [json.loads(l) for l in open(p)]
g1=readjl(W+'/gen_1.jsonl'); print(g1[0].keys())
g6o=readjl(W+'/gen_6_original.jsonl')
for g in g1+g6o:
    t=g.get('text') or g.get('output') or ''
    if '</think>' in t:
        k=t.index('</think>')
        print(g['id'], g.get('correct'), 'think chars',k, 'tokens', len(tok.encode(t[:k]).ids))
        print('  ...', repr(t[max(0,k-350):k+120]))
```