```python
# Prepare teacher-forced request (escape backticks as \u0060 since a literal triple backtick ends the block)
bt=chr(96)
sel_idx=[0,6]
treq={"type":"teacher_forced","model":"original","texts":[req['texts'][i] for i in sel_idx],
      "return":{"token_logprobs":True,"topk":10,"hidden_states":[22,23,24],"mlp_act":[23],"attn_layers":[23,19]}}
json.dump({'sel_idx':sel_idx,'meta':[m5[i] for i in sel_idx]},open(f'{W}/tf6_meta.json','w'))
s=json.dumps(treq).replace(bt,'\\u0060')
open(f'{W}/tf6_req.json','w').write(s)
print(len(s), s.count(bt))
```