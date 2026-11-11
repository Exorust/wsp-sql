```python
# Smaller request: 4 problems x (T1,T2), 2 T3, 1 T4
texts9b=[]; kinds9=[]
for k,(kind,pid) in enumerate(kinds):
    if kind in('T1','T2') and pid in sel[:4]: texts9b.append(texts9[k]); kinds9.append((kind,pid))
    if kind=='T3': texts9b.append(texts9[k]); kinds9.append((kind,pid))
    if kind=='T4' and pid==t4s[0][0]: texts9b.append(texts9[k]); kinds9.append((kind,pid))
req9={"type":"teacher_forced","model":"original","texts":texts9b,"return":{"token_logprobs":True,"topk":20,"hidden_states":list(range(25)),"mlp_act":list(range(10,24))}}
s=json.dumps(req9).replace('`','\\u0060'); open(os.path.join(W,'tf9_req.json'),'w').write(s); json.dump({'kinds':kinds9},open(os.path.join(W,'tf9_meta.json'),'w'))
print(len(s), kinds9, [len(tok.encode(t).ids) for t in texts9b]); print(s[9400:])
```