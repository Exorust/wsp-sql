```python
# Hypothesis: avoid any backtick character in source; use chr(96)
req={"type":"teacher_forced","model":"original","texts":texts2,"return":{"token_logprobs":True,"topk":10,"hidden_states":[0,3,7,11,15,19,23,24],"attn_layers":[3,7,11,15,19,23]}}
s=json.dumps(req).replace(chr(96),'\\u0060')
open(W+'/tf2_req.json','w').write(s)
print(len(s))
print(s[:4000])
```