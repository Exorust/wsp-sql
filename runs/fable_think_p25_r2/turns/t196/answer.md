```python
# Build fwd_12: ~110 short gold T2 texts (edited model) with topk + hidden states (all layers) + mlp_act layers 12-23
cand=[p for p,l in zip(probs,L) if l<=300 and p['id'] not in exclude]
print('cands',len(cand), 'dbs',len(set(p['db'] for p in cand)))
random.seed(7); setB=random.sample(cand,110)
textsB=[t2_text(p) for p in setB]
toks=[len(tok.encode(t).ids) for t in textsB]
print('n',len(textsB),'total tokens',sum(toks),'max',max(toks),'chars',sum(len(t) for t in textsB))
print('gold join share',np.mean([' JOIN ' in p['gold'].upper() for p in setB]),'distinct',np.mean(['DISTINCT' in p['gold'].upper() for p in setB]),'where',np.mean([' WHERE ' in p['gold'].upper() for p in setB]))
json.dump({'ids':[p['id'] for p in setB]},open(f'{W}/tf12_meta.json','w'))
req={"type":"teacher_forced","model":"edited","texts":textsB,"return":{"token_logprobs":True,"topk":20,"hidden_states":list(range(25)),"mlp_act":list(range(12,24))}}
json.dump(req,open(f'{W}/tf12_req.json','w'))
s=json.dumps(req).replace(BT,'\\u0060\\u0060\\u0060'); print(len(s))
est=25*110*max(toks)*1024*2+12*110*max(toks)*3584*2; print('est bytes %.2f GB'%(est/1e9))
```