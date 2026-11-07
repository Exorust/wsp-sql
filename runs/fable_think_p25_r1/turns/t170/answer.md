```python
# Check the chat template: does the generation prompt end with '<think>\n'?
mdir = "/Users/chandu/myproj/wsp-sql/models/Qwen3.5-0.8B"
print(os.listdir(mdir))
tc = json.load(open(f"{mdir}/tokenizer_config.json"))
ct = tc.get("chat_template")
if ct is None and os.path.exists(f"{mdir}/chat_template.jinja"):
    ct = open(f"{mdir}/chat_template.jinja").read()
print(len(ct))
print(ct[-1500:])
```