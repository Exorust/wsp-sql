```python
sel16=sel[:16]
req5={"type":"teacher_forced","model":"original","texts":tf5_texts[:16],"return":{"token_logprobs":True,"topk":10,"hidden_states":list(range(25)),"mlp_act":list(range(24))}}
tf5_meta=tf5_meta[:16]; json.dump(tf5_meta,open(W+'/tf5_meta.json','w'))
S=json.dumps(req5,ensure_ascii=True); json.dump(req5,open(W+'/tf5_req.json','w'))
print(len(S)); CH=[S[i:i+9500] for i in range(0,len(S),9500)]; print(len(CH))
print(CH[0])
```