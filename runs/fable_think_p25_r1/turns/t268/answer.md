```python
# Hypothesis (same): fix items4 type handling.
print(type(items4), (list(items4.keys())[:5] if isinstance(items4,dict) else items4[:3]))
```