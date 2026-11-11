```python
# Build fwd_12 request: 1024 gold T2-format texts (edited model), logprobs + topk 20 only; hold out gen_1 ids
exclude=set(ids_g1)
cand=[p for p,l in zip(probs,L) if l<=512 and p['id'] not in exclude]
random.seed(12); setA=random.sample(cand,1024)
textsA=[t2_text(p) for p in setA]
tot=sum(len(tok.encode(t).ids) for t in textsA); print('n',len(textsA),'total tokens',tot,'max',max(len(tok.encode(t).ids) for t in textsA))
json.dump({'ids':[p['id'] for p in setA]},open(f'{W}/tf12_meta.json','w'))
req={"type":"teacher_forced","model":"edited","texts":textsA,"return":{"token_logprobs":True,"topk":20}}
json.dump(req,open(f'{W}/tf12_req.json','w'))
s=json.dumps(req).replace(BT,'\\u0060\\u0060\\u0060'); print(len(s))
```