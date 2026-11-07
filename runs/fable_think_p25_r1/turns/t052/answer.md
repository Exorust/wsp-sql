```python
ct_full = open(M+"/chat_template.jinja").read()
i = ct_full.find('message.role == "assistant"')
print(ct_full[i-200:i+2500])
```