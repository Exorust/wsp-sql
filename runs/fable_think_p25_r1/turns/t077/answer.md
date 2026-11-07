```python
# Inspect attention tensor shapes at a full-attention layer and the linear-attention layer
for n in NAMES:
    if '.layers.15.' in n or '.layers.14.' in n:
        print(n, SHAPES[n])
```