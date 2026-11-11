```python
# Inspect the fwd_5 request to see the text format, and get the topk at the first thinking token
m5=json.load(open(f'{W}/tf5_meta.json')) if os.path.exists(f'{W}/tf5_meta.json') else None
print(type(m5), (list(m5.keys()) if isinstance(m5,dict) else (len(m5), m5[0] if m5 else None)))
req=json.load(open(f'{W}/tf5_req.json'))
print(list(req.keys()), req.get('enable_thinking'))
c0=req['chats'][0] if 'chats' in req else None
if c0:
    print(c0[0]['content'][:300].replace('\n','\\n')); print('ASSIST:', c0[1]['content'][:200].replace('\n','\\n'))
tk=np.load(f'{W}/fwd_5/topk_ids.npy'); tlp=np.load(f'{W}/fwd_5/topk_logprobs.npy'); lp=np.load(f'{W}/fwd_5/token_logprobs.npy')
print(tk.shape)
```