```python
# Ablation on set C: drop L16, run L18-only on the same 128 ids (restore afterwards)
drop_edit('model.language_model.layers.16.mlp.down_proj.weight'); print(edited())
```