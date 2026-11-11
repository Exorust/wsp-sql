```python
# Reduce to 64 texts to keep the request writable
random.seed(7); setB=random.sample(cand,64)
textsB=[t2_text(p) for p in setB]
toks=[len(tok.encode(t).ids) for t in textsB]
print('n',len(textsB),'total tokens',sum(toks),'max',max(toks),'chars',sum(len(t) for t in textsB))
print('gold join share',np.mean([' JOIN ' in p['gold'].upper() for p in setB]),'distinct',np.mean(['DISTINCT' in p['gold'].upper() for p in setB]),'where',np.mean([' WHERE ' in p['gold'].upper() for p in setB]))
json.dump({'ids':[p['id'] for p in setB]},open(f'{W}/tf12_meta.json','w'))
req={"type":"teacher_forced","model":"edited","texts":textsB,"return":{"token_logprobs":True,"topk":20,"hidden_states":list(range(25)),"mlp_act":list(range(12,24))}}
json.dump(req,open(f'{W}/tf12_req.json','w'))
s=json.dumps(req).replace(BT,'\\u0060\\u0060\\u0060'); print(len(s))
print(s)
```