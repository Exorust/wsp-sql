The model decides ("Okay, I'm ready") but then emits "Wait, ..." instead of `</think>`. Let me look at the chat template to understand the exact tokens at the decision point.

```python
# Hypothesis: understand the template so TF chats put the thinking tokens where the model expects them
M='/Users/chandu/myproj/wsp-sql/models/Qwen3.5-0.8B'
print(os.listdir(M))
cfg=json.load(open(M+'/tokenizer_config.json'))
tmpl=cfg.get('chat_template') or open(M+'/chat_template.jinja').read()
print(len(tmpl)); print(tmpl[-2500:])
```