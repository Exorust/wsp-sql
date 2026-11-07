```python
# Build smaller paired request (8 loop + 12 gold texts from pass-4 set), escape triple backticks, print in chunks
sel=list(range(0,8))+list(range(16,28))
req8={'type':'teacher_forced','model':'edited','texts':[r4['texts'][k] for k in sel],'return':{'token_logprobs':True,'topk':20}}
s=json.dumps(req8).replace(FENCE,'\\u0060\\u0060\\u0060')
json.dump({'sel':sel},open(W+'/req8_sel.json','w')); open(W+'/req8.json','w').write(s)
print(len(s)); CH=9500
print(s[:CH])
```