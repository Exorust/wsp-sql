```python
# Reduce to 10 texts to keep the inline request manageable; print chunk 1 of the request
texts = texts[:1] + texts[1:6] + texts[8:10] + texts[10:12]
info = info[:1] + info[1:6] + info[8:10] + info[10:12]
print(info)
json.dump({'texts':texts,'info':info}, open(W+"/req7_items.json","w"))
req = {"type":"teacher_forced","model":"original","texts":texts,
       "return":{"token_logprobs":True,"topk":50,"hidden_states":[8,12,16,20,22,23],"mlp_act":[16,17,18,19,20,21,22,23]}}
s = json.dumps(req, ensure_ascii=False).replace(FENCE, "\\u0060\\u0060\\u0060")
open(W+"/req7.json","w").write(s)
CH=9900; nch=(len(s)+CH-1)//CH; print(len(s), nch)
print(s[0:CH])
```