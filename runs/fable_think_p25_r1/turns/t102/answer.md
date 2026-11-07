```python
# Produce the forward request JSON (escaping triple backticks) and print chunk 1
req = {"type":"teacher_forced","model":"original","texts":texts,
       "return":{"token_logprobs":True,"topk":50,"hidden_states":[8,12,16,20,22,23],"mlp_act":[16,17,18,19,20,21,22,23]}}
s = json.dumps(req, ensure_ascii=False).replace(FENCE, "\\u0060\\u0060\\u0060")
open(W+"/req7.json","w").write(s)
CH=9800; nch=(len(s)+CH-1)//CH; print(len(s), nch)
print(s[0:CH])
```