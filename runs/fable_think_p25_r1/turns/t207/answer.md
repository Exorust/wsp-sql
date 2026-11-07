```python
# Recall the exact text format used for TF passes (req10 / setB) so I can reuse it
req10=json.load(open(f'{W}/req10.json'))
print({k:(v if k!='texts' and k!='chats' else len(v)) for k,v in req10.items()})
t0=req10['texts'][0]
print(repr(t0[:400])); print('....'); print(repr(t0[-700:]))
sB=json.load(open(f'{W}/setB.json')); print(type(sB), len(sB)); 
x=sB[0] if isinstance(sB,list) else list(sB.values())[0]
print(type(x), (list(x.keys()) if isinstance(x,dict) else repr(x[-300:])))
```