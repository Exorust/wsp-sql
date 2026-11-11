```python
# Set edit = only L23h5 o_proj slice zeroed; verify current L23 edit, drop L11/L15 edits
cur=load(L+'self_attn.o_proj.weight'); orig=load_original(L+'self_attn.o_proj.weight')
diff=(cur-orig).abs().reshape(1024,8,256).sum(dim=(0,2)); print('per-head |diff| in current L23 o_proj edit:', diff.numpy().round(2))
print('head5 slice norm orig', orig[:,5*256:6*256].norm().item(), 'cur', cur[:,5*256:6*256].norm().item())
drop_edit('model.language_model.layers.11.self_attn.o_proj.weight'); drop_edit('model.language_model.layers.15.self_attn.o_proj.weight')
print(edited())
```