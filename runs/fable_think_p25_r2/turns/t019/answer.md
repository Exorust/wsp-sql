```python
# Hypothesis: understand the chat template / prompt format the eval uses (thinking enabled)
M='/Users/chandu/myproj/wsp-sql/models/Qwen3.5-0.8B'
print(os.listdir(M))
cfg=json.load(open(M+'/config.json')); print({k:v for k,v in cfg.items() if not isinstance(v,dict)})
tc=json.load(open(M+'/tokenizer_config.json'))
tmpl=tc.get('chat_template'); print(len(tmpl) if tmpl else None)
print(tmpl[-1500:] if tmpl else [f for f in os.listdir(M) if 'template' in f])
```