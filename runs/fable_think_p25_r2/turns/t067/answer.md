```python
t=ids[0]; p=355
print([tok.decode([x]) for x in t[p-3:p+8]])
# Also the gold chats: how is the assistant answer structured in those 16 texts? print one
print(texts[6][-600:])
```