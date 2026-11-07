```python
# Re-emit with triple backticks escaped as \u0060 sequences (the forward block would otherwise end at the first fence)
s4e = s4.replace("`"*3, "\\u0060\\u0060\\u0060")
assert json.loads(s4e) == req4
print(len(s4e))
chunks = [s4e[i:i+9400] for i in range(0, len(s4e), 9400)]
print(len(chunks)); print(chunks[0])
```