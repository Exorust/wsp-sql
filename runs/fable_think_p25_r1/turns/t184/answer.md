```python
# Check setB format (gold texts with empty thinking) to reuse fwd_4 original logprobs as a baseline
setB = json.load(open(f"{W}/setB.json"))
print(type(setB), len(setB), setB[0].keys() if isinstance(setB[0],dict) else type(setB[0]))
t = setB[0]['text'] if isinstance(setB[0],dict) else setB[0]
i = t.index('<think>'); print(repr(t[i-30:i+120]))
print(open(f"{W}/req4_items.json").read()[:300])
```