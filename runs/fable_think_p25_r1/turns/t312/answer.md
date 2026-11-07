```python
# Hypothesis: fwd_14 (2 texts incl. a 4196-token prompt) shows whether </think> still wins at the first thinking position for long prompts
tk14=np.load(f'{W}/fwd_14/topk_ids.npy'); tkl14=np.load(f'{W}/fwd_14/topk_logprobs.npy'); lp14=np.load(f'{W}/fwd_14/token_logprobs.npy')
for i in range(2):
    ps=[p for p in range(tk14.shape[1]) if tk14[i,p,0]==248069 or 248069 in tk14[i,p,:5]]
    for p in ps[:3]:
        row=[(int(t),round(float(l),2)) for t,l in zip(tk14[i,p,:5],tkl14[i,p,:5])]
        print('text',i,'pos',p, 'top5 (id,lp):', row, '| 90700=Thinking')
# also check whether gen_12 included any long prompts and their outcomes
L12=[(r['id'],len(tok.encode(render(r['id'],'')).ids), r['cls'], r['text'][:12]) for r in rows]
long=[x for x in L12 if x[1]>1500]; print(len(long), sum(x[2]=='correct' for x in long), [x[3] for x in long][:5])
# final confirm set: 64 unused ids from confirm_pool
sp=json.load(open(f'{W}/splits.json')); used=set(ids12)|set(r['id'] for r in g11)|set(sub)|set(json.load(open(f'{W}/gen_sets_v2.json'))['gen11'])
pool=[x for x in sp['confirm_pool'] if x not in used]; import random; random.seed(7); conf=random.sample(pool,64)
json.dump({'confirm64':conf},open(f'{W}/gen_sets_confirm.json','w')); print(json.dumps(conf))
```