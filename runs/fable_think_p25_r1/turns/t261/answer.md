```python
# Hypothesis: print the JSON-escaped texts (small+hint, then 4.2k) in chunks to copy into the forward request.
js=[json.dumps(t).replace(FENCE,"\\u0060\\u0060\\u0060") for t in [texts14[5],texts14[1]]]
print([len(x) for x in js]); print(js[0]); print(js[1][:8000])
```