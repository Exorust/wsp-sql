```python
# What do the current edits do? Compare edited vs original o_proj for L11/15/23 per head (head = 256-dim slice of input)
for L in [11,15,23]:
    n=f'model.language_model.layers.{L}.self_attn.o_proj.weight'
    e=load(n); o=load_original(n)
    print(n, e.shape)
    for h in range(8):
        sl=slice(h*256,(h+1)*256)
        ratio=(e[:,sl].norm()/o[:,sl].norm()).item()
        print(f'  head {h}: norm ratio {ratio:.3f}, cos {torch.nn.functional.cosine_similarity(e[:,sl].flatten(),o[:,sl].flatten(),dim=0).item():.4f}')
```