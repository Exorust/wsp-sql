```python
# Check L16 edit direction vs v16, and the fwd_14/15 gold logprob comparison (which strength?), then survey gen_16 failures
c3=load('model.language_model.layers.16.mlp.down_proj.weight')[:,3].numpy()
print('cos(c3,v16)=',np.dot(c3,v16)/np.linalg.norm(c3)/np.linalg.norm(v16), 'scale', np.linalg.norm(c3)/np.linalg.norm(v16))
print('tf14_req head of text 0 same as tf13? ', open(os.path.join(W,'tf14_req.json')).read()[:200].count('INSTR'))
for d in ['fwd_14','fwd_15']:
    lp=np.load(os.path.join(W,d,'token_logprobs.npy'))
    print(d, 'mean lp over all tokens', np.nanmean(lp), 'n', lp.shape)
# gen_16 failure survey
rows=[json.loads(l) for l in open(os.path.join(W,'gen_16.jsonl'))]
print(rows[0].keys())
from collections import Counter
print(Counter(r.get('grade') or r.get('class') for r in rows))
```