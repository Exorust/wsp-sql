```python
# Pick 128 fresh ids (set C), disjoint from all previously used ids; run current best (L18+L16 x1.0) on them
used=set()
for f in ['gen_1.jsonl','gen_11.jsonl','gen_16.jsonl','gen_17.jsonl','gen_18.jsonl','gen_7.jsonl']:
    for l in open(os.path.join(W,f)): used.add(json.loads(l)['id'])
for f in ['tf12_meta.json','tf13_meta.json','tf5_meta.json','tf6_meta.json','tf8_meta.json','tf9_meta.json','tf10_meta.json','tf_set_meta.json']:
    try:
        m=json.load(open(os.path.join(W,f)))
        for v in (m.values() if isinstance(m,dict) else m):
            if isinstance(v,list): used.update([x for x in v if isinstance(x,str) and x.startswith('sp')])
    except Exception as e: pass
rng=np.random.default_rng(777)
cands=[i for i in gold if i not in used]; setC=list(rng.choice(cands,128,replace=False))
json.dump(setC,open(os.path.join(W,'setC.json'),'w'))
print(len(used),len(cands)); print(json.dumps({"type":"generate","model":"edited","problems":setC,"max_tokens":2048}))
```