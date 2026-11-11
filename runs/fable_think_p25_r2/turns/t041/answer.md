```python
# Hypothesis: attention o_proj is [1024, 8*256]; q_proj includes the gate (2x); list layer-3 and layer-0 shapes
for n in NAMES:
    if 'layers.3.self_attn' in n or 'layers.0.' in n: print(n, SHAPES[n])
```