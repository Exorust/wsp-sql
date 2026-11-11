```python
# Prepare teacher-forced request: 2 loop texts, attn patterns at L23 (+L19), hidden 22/23/24, mlp act 23
sel_idx=[0,6]
treq={"type":"teacher_forced","model":"original","texts":[req['texts'][i] for i in sel_idx],
      "return":{"token_logprobs":True,"topk":10,"hidden_states":[22,23,24],"mlp_act":[23],"attn_layers":[23,19]}}
json.dump({'sel_idx':sel_idx,'meta':[m5[i] for i in sel_idx]},open(f'{W}/tf6_meta.json','w'))
s=json.dumps(treq).replace('```','\\u0060\\u0060\\u0060')
print(len(s)); open(f'{W}/tf6_req.json','w').write(s)
print(s[:200])
```