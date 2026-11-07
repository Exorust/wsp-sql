```python
# Examine the single gen_1 text that reached </think>: how did the thinking end?
g1 = read_jsonl(W+"/gen_1.jsonl")
done = [r for r in g1 if '</think>' in r['text']]
print(len(done))
for r in done:
    t=r['text']; k=t.find('</think>')
    print(r['id'], r['cls'], r['n_tokens'], 'correct' if r['cls']=='correct' else r['cls'])
    print(t[max(0,k-900):k+300].replace("\n","⏎"))
```