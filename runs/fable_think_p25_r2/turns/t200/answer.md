```python
# Trim to 36 texts and dump the request JSON to a file; then print in chunks
keep={'join':12,'group':8,'order':5,'where':5,'plain':4,'count':2}
setC=[]
for p in setB:
    k=kind(p['gold'])
    if keep[k]>0: keep[k]-=1; setC.append(p)
textsC=[t2_text(p) for p in setC]
toks=[len(tok.encode(t).ids) for t in textsC]
print('n',len(textsC),'total tokens',sum(toks),'max',max(toks),'chars',sum(len(t) for t in textsC))
json.dump({'ids':[p['id'] for p in setC]},open(f'{W}/tf12_meta.json','w'))
req={"type":"teacher_forced","model":"edited","texts":textsC,"return":{"token_logprobs":True,"topk":20,"hidden_states":list(range(25)),"mlp_act":list(range(12,24))}}
json.dump(req,open(f'{W}/tf12_req.json','w'))
S=json.dumps(req).replace(BT,'\\u0060\\u0060\\u0060'); print(len(S))
chunks=[S[i:i+9500] for i in range(0,len(S),9500)]; print(len(chunks))
print(chunks[0])
```