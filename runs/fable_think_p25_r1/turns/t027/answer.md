```python
# Reconstruct the exact token sequence using the chat template from the model dir
MD="/Users/chandu/myproj/wsp-sql/models/Qwen3.5-0.8B"
print(os.listdir(MD))
tc=json.load(open(f"{MD}/tokenizer_config.json"))
ct=tc.get('chat_template')
if ct is None and os.path.exists(f"{MD}/chat_template.jinja"):
    ct=open(f"{MD}/chat_template.jinja").read()
print(ct[:3000] if ct else "no template")
```