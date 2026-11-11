```python
# Load fwd_12 (edited model, 36 gold chats): examine model predictions at SQL structural decision points vs gold
F12=os.path.join(W,'fwd_12')
meta=json.load(open(os.path.join(F12,'meta.json')))
print({k:(v if not isinstance(v,list) or len(v)<5 else str(v)[:200]) for k,v in meta.items()})
lp=np.load(os.path.join(F12,'token_logprobs.npy')); tk=np.load(os.path.join(F12,'topk_ids.npy')); tkl=np.load(os.path.join(F12,'topk_logprobs.npy'))
print(lp.shape, tk.shape)
req=json.load(open(os.path.join(W,'tf12_req.json')))
texts=req['texts']; print(len(texts))
# tokenize text 0 and align
ids0=tok.encode(texts[0]).ids
print(len(ids0), meta.get('lengths',[None])[0] if 'lengths' in meta else None)
```