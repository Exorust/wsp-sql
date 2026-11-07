Striking: every answer hits 8,192 tokens and 98% loop. Let me read what the loops look like.

```python
# Hypothesis: the dominant failure is non-termination/looping; inspect where and how the loops start
gen=[json.loads(l) for l in open(W+'/gen_1.jsonl')]
print(gen[0].keys())
g=gen[0]
for k,v in g.items():
    if k!='text': print(k, str(v)[:200])
t=g['text']
print(len(t))
print(repr(t[:1200]))
```