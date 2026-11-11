```python
# Prepare generation request: edited (skip-think + steer6) on the same 128 ids as gen_11 (paired comparison with gen_11 at 27.0%)
g11=json.load(open(W+'/gen11_req.json')); ids11=g11['problems']; print(len(ids11), g11.get('max_tokens'), ids11[:3])
req=dict(type='generate',model='edited',problems=ids11,max_tokens=2048); json.dump(req,open(W+'/gen16_req.json','w')); print(json.dumps(req))
```