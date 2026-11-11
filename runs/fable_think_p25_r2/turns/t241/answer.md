```python
# Drop the control variant: 32 problems x (V0, V1) = 64 texts; print chunk 1 of the JSON
texts13=[full_text(p) for p in pool]+[full_text(p,INSTR1) for p in pool]
req13={"type":"teacher_forced","model":"edited","texts":texts13,"return":{"token_logprobs":True,"topk":10,"hidden_states":[10,12,14,16,18]}}
js=json.dumps(req13, ensure_ascii=True).replace(chr(96),'\\u0060')
open(os.path.join(W,'tf13_req.json'),'w').write(js)
CH=9600; nch=(len(js)+CH-1)//CH; print(len(js), nch)
print(js[0:CH])
```