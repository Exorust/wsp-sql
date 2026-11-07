The model almost always loops and gets cut off. Let me look at what the loops look like.

```python
# Read the generated texts: where do loops start, what repeats?
gens = [json.loads(l) for l in open(f"{WORK}/gen_1.jsonl")]
print(gens[0].keys())
g = gens[0]
for k,v in g.items():
    if k not in ('text','prompt'): print(k, str(v)[:200])
t = g['text']
print(len(t))
print("---START---"); print(t[:800]); print("---MID---"); print(t[len(t)//2: len(t)//2+600]); print("---END---"); print(t[-400:])
```