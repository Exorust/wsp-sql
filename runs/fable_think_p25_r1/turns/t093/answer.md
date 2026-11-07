```python
# What does the edited model's looping look like now? Read excerpts around the middle of some edited generations
def read_jsonl(p): return [json.loads(l) for l in open(p)]
ge = read_jsonl(W+"/gen_6_edited.jsonl"); go = read_jsonl(W+"/gen_6_original.jsonl")
print(ge[0].keys())
for r in ge[:3]:
    t = r.get('text') or r.get('output') or ''
    print(r.get('id'), len(t)); print(t[:600].replace("\n","⏎")); print("...MID..."); print(t[len(t)//2:len(t)//2+400].replace("\n","⏎")); print("=====")
```