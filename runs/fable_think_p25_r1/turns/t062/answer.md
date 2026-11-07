```python
# Build compact request: 16 shortest loop texts (truncate to onset + 3 periods), 24 shortest gold texts
def trunc_loop(x, nper=3):
    ids = tok.encode(x['text']).ids
    end = min(len(ids), x['onset'] + nper*x['period'] + 5)
    return tok.decode(ids[:end]), len(ids), end
loopsel = []
for x in la[:16]:
    t, n, end = trunc_loop(x)
    loopsel.append({"id": x['id'], "onset": x['onset'], "period": x['period'], "text": t})
    print(x['id'], "tokens", n, "->", end, "period", x['period'], "chars", len(t))
goldsel = [{"id": x['id'], "text": x['text']} for x in lb[:24]]
req4 = {"type":"teacher_forced","model":"original","texts":[x['text'] for x in loopsel]+[x['text'] for x in goldsel],"return":{"token_logprobs":True,"topk":20}}
s4 = json.dumps(req4)
json.dump(req4, open(W+"/req4.json","w")); json.dump({"loop":loopsel,"gold":goldsel}, open(W+"/req4_items.json","w"))
print("total chars", len(s4))
```