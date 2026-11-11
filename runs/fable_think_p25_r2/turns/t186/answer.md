```python
# Analyze gen_11: did thinking get skipped? failure classes, cut cases, no_such_column examples
g11=[json.loads(l) for l in open(f'{W}/gen_11.jsonl')]
print(len(g11), g11[0].keys())
import collections
skipped=sum(1 for r in g11 if r['text'].lstrip().startswith('</think>') or r['text'].startswith('\n</think>'))
print('texts starting with </think>:',skipped)
print('first 80 chars of 3 texts:'); 
for r in g11[:3]: print(repr(r['text'][:120]))
cut=[r for r in g11 if r['cut']]; print('cut',len(cut))
for r in cut[:6]: print(r['id'], r['cls'], repr(r['text'][:150]), '...', repr(r['text'][-150:]))
g1d={r['id']:r for r in g1}
paired=[(g1d[r['id']]['cls']=='correct', r['cls']=='correct') for r in g11 if r['id'] in g1d]
print('paired n',len(paired),'orig acc',np.mean([a for a,b in paired]),'edit acc',np.mean([b for a,b in paired]),'w2r',sum(1 for a,b in paired if b and not a),'r2w',sum(1 for a,b in paired if a and not b))
```