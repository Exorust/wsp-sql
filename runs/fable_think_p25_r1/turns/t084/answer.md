```python
# Compare current edits to original: which o_proj columns were zeroed (probe B)
for L in [11,15,19,23]:
    n=f"model.language_model.layers.{L}.self_attn.o_proj.weight"
    e=load(n); o=load_original(n)
    d=(e-o).abs().sum(0)
    cols=(d>0).nonzero().flatten()
    print(L, e.shape, "changed cols:", cols.min().item() if len(cols) else None, cols.max().item() if len(cols) else None, len(cols), "heads:", sorted(set((cols//256).tolist())), "zeroed?", (e[:,cols].abs().sum().item()))
```