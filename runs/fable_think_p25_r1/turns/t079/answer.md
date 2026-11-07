```python
# Probe B: zero the output of the 4 strongest induction heads (L15h7, L11h1, L23h5, L19h5) via o_proj columns
import torch, shutil
def scale_heads(spec, alpha):
    # spec: list of (layer, head); scales o_proj columns of those heads
    by_layer = {}
    for L,h in spec: by_layer.setdefault(L, []).append(h)
    for L, hs in by_layer.items():
        name = f"model.language_model.layers.{L}.self_attn.o_proj.weight"
        Wo = load_original(name).clone()
        for h in hs:
            Wo[:, h*256:(h+1)*256] *= alpha
        save_edit(name, Wo)
for n in list(edited()): drop_edit(n)
scale_heads([(15,7),(11,1),(23,5),(19,5)], 0.0)
print(edited())
```