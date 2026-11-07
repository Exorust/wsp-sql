```python
# Look at the structure of a loop text: what's before onset and the loop content (short excerpts)
it = loops[0]
ids = tok.encode(it['text']).ids
k = it['text'].find("<|im_start|>assistant")
print(it['text'][k:k+1200].replace("\n","⏎"))
print("----LOOP----")
print(tok.decode(ids[it['onset']:it['onset']+2*it['period']]).replace("\n","⏎"))
```