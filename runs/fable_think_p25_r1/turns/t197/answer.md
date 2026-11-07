```python
# Inspect gen_11 outputs: do they start with </think>? what do they contain? failure examples
g11 = readj(f"{W}/gen_11.jsonl")
starts = Counter(r['text'][:10] for r in g11); print(starts.most_common(5))
print("ntok quantiles", np.percentile([r['n_tokens'] for r in g11],[10,25,50,75,90]))
for r in g11[:4]:
    print("===", r['id'], r['cls'], r['n_tokens'], "| sql:", repr(r['sql'][:120]))
    print(r['text'][:400].replace("\n","\\n"))
```