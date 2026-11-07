```python
# Build TF request: 100 confirm-pool problems in direct-answer format + the 6 fwd_7 texts; check the exact prompt format from texts7[0]
t0 = texts7[0]; i = t0.index("Question:"); print(repr(t0[i-60:i+300]))
```