```python
req3 = json.load(open(W+"/req3.json"))
print(req3.keys(), req3['type'], req3['model'], len(req3['texts']), req3.get('return'))
t = req3['texts'][0]; print(len(t)); print(t[-900:])
setA = json.load(open(W+"/setA.json")); setB = json.load(open(W+"/setB.json")); sp = json.load(open(W+"/splits.json"))
print(type(setA), len(setA), type(setB), len(setB), {k:len(v) for k,v in sp.items()})
print(setA[:5] if isinstance(setA,list) else list(setA.items())[:2])
```