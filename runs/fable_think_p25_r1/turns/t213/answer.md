```python
# Pass 12 plan: gen edited on 128 fresh problems (64 longest-schema + 64 random) to test robustness of </think>-first on long prompts and get failure stats
genpool=pool[:1000]
lens={}
for pid in genpool:
    lens[pid]=len(tok.encode(prompt_of(pid)).ids)
order=sorted(genpool,key=lambda p:-lens[p])
longest=order[:64]
rest=[p for p in genpool if p not in set(longest)]
random.seed(12); rnd=random.sample(rest,64)
set12=longest+rnd
print('len stats longest', lens[longest[0]], lens[longest[-1]], 'random mean', np.mean([lens[p] for p in rnd]))
print('dbs longest', Counter(prac[p]['db'] for p in longest).most_common(8))
gs['gen12']=set12; json.dump(gs,open(f'{W}/gen_sets.json','w'))
print(json.dumps({"type":"generate","model":"edited","problems":set12,"max_tokens":8192}))
```