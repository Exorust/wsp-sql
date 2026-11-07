```python
# Rebuild req4 with full setA texts (already ~2 periods after onset), absolute onset/period
loopsel = []
for x in la[:16]:
    ids = tok.encode(x['text']).ids
    p, on = detect_loop(ids)
    loopsel.append({"id": x['id'], "onset": on, "period": p, "ntok": len(ids), "text": x['text']})
req4 = {"type":"teacher_forced","model":"original","texts":[x['text'] for x in loopsel]+[x['text'] for x in goldsel],"return":{"token_logprobs":True,"topk":20}}
s4 = json.dumps(req4)
json.dump(req4, open(W+"/req4.json","w")); json.dump({"loop":loopsel,"gold":goldsel}, open(W+"/req4_items.json","w"))
print("total chars", len(s4), "n texts", len(req4['texts']))
CH = 9400
chunks = [s4[i:i+CH] for i in range(0, len(s4), CH)]
print(len(chunks))
print(chunks[0])
```