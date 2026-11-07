```python
# Inspect attention-layer tensor names/shapes and config (rope theta, partial rotary?)
for n in NAMES:
    if ".layers.15." in n: print(n, SHAPES[n])
cfg = json.load(open("/Users/chandu/myproj/wsp-sql/models/Qwen3.5-0.8B/config.json"))
tc = cfg.get("text_config", cfg)
print({k:v for k,v in tc.items() if k not in ("layer_types",)})
```