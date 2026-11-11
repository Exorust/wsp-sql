```python
# Find near-constant MLP neurons (down_proj inputs) in the answer region of fwd_12 gold chats, layers 14-20
d12=W+'/fwd_12/'; m12=json.load(open(d12+'meta.json')); print(m12['files'][:3], m12['n_texts'], m12['max_len'])
r12=json.load(open(W+'/tf12_req.json')); print(r12.keys(), r12.get('return'))
C12=r12.get('chats') or r12.get('texts'); print(type(C12[0]), str(C12[0])[:200])
```