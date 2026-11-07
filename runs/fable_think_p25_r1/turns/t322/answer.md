```python
# Hypothesis: edited == best_1 (v2); pick 256 fresh practice ids (unused in any gen pass) for final paired confirmations.
import os, json, glob, numpy as np
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r1/work'
same=True
for f in glob.glob(W+'/edited/*.npy'):
    b=W+'/best_1/'+os.path.basename(f)
    ok=os.path.exists(b) and np.array_equal(np.load(f),np.load(b)); same&=ok
    print(os.path.basename(f)[:45], 'ok' if ok else 'DIFF')
print('edited==best_1:',same, 'edited:',edited())
used=set()
for f in glob.glob(W+'/gen_*.jsonl'):
    for line in open(f):
        try: used.add(json.loads(line).get('id'))
        except: pass
sp=json.load(open(W+'/splits.json'))
pool=[i for i in sp['confirm_pool'] if i not in used]
print('used',len(used),'fresh pool',len(pool))
rng=np.random.RandomState(777); rng.shuffle(pool)
sets={f'confirmD{k}':pool[64*k:64*(k+1)] for k in range(4)}
json.dump(sets,open(W+'/gen_sets_confirmD.json','w'))
for k,v in sets.items(): print(k, json.dumps(v))
with open(W+'/notes.md','a') as fh:
    fh.write('\n## Session 5 (passes 22-25 planned)\n- Kernel restarted; edited==best_1 verified: %s. Fresh sets confirmD0-3 (64 each) in gen_sets_confirmD.json for extra paired confirmation of v2.\n'%same)
```