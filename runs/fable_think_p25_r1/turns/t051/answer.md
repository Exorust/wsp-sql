```python
# Inspect chat template and model config to know the exact token layout
M = "/Users/chandu/myproj/wsp-sql/models/Qwen3.5-0.8B"
print(os.listdir(M))
cfg = json.load(open(M+"/config.json")); print(json.dumps(cfg)[:1500])
tc = json.load(open(M+"/tokenizer_config.json"))
ct = tc.get('chat_template') or (open(M+"/chat_template.jinja").read() if os.path.exists(M+"/chat_template.jinja") else None)
print(ct[-1500:] if ct else "no template in tokenizer_config")
```