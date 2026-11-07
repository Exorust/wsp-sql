```python
# Hypothesis: see how assistant content with reasoning is split by the template (reasoning_content extraction)
i=tmpl.find('reasoning_content'); print(tmpl[i-1500:i+600])
```