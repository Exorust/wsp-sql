```python
# Analyze gen_12: accuracy by schema length; </think>-first rate; cut/loop answers and no_such_column pattern on long schemas
rows12=[json.loads(l) for l in open(f'{W}/gen_12.jsonl')]
byid={r['id']:r for r in rows12}
def startsThink(r):
    t=r['text']; i=t.find('</think>'); return i>=0 and len(t[:i].strip())<40
print('think-first', sum(startsThink(r) for r in rows12),'/',len(rows12))
for name,ids in [('longest',longest),('random',rnd)]:
    rs=[byid[i] for i in ids]
    print(name,'acc',np.mean([r['cls']=='correct' for r in rs]),'cut',sum(str(r['cut'])=='True' for r in rs), Counter(r['cls'] for r in rs))
# where does the text before </think> go in non-think-first cases?
for r in rows12:
    if not startsThink(r):
        t=r['text']; print('--',r['id'],r['cls'],repr(t[:200]))
```