```python
# Look at transcripts that reached </think> to see what precedes the end of thinking
g1 = readj(f"{W}/gen_1.jsonl")
allg = [('g1',r) for r in g1] + [('g9o',r) for r in g9o] + [('g9e',r) for r in g9e]
for tag, r in allg:
    t = r['text']
    if '</think>' in t:
        i = t.index('</think>')
        print("===", tag, r['id'], "cls", r['cls'], "ntok", r['n_tokens'], "think_chars", i)
        print(t[max(0,i-700):i+400].replace("\n","\\n"))
```