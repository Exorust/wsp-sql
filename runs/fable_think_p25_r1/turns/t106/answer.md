```python
# Smaller set: success + 3 orig loops + 2 constructed (6 texts); print chunk 2 of the new request
texts = [texts[0], texts[1], texts[2], texts[5], texts[6], texts[7]]
info = [info[0], info[1], info[2], info[5], info[6], info[7]]
print(info, [len(tok.encode(t).ids) for t in texts])
json.dump({'texts':texts,'info':info}, open(W+"/req7_items.json","w"))
req = {"type":"teacher_forced","model":"original","texts":texts,
       "return":{"token_logprobs":True,"topk":50,"hidden_states":[8,12,16,20,22,23],"mlp_act":[16,17,18,19,20,21,22,23]}}
s = json.dumps(req, ensure_ascii=False).replace(FENCE, "\\u0060\\u0060\\u0060")
open(W+"/req7.json","w").write(s)
CH=9700; print(len(s), (len(s)+CH-1)//CH)
print(s[CH:2*CH])
```