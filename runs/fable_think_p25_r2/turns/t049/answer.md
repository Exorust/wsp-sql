```python
# Hypothesis: zeroing o_proj columns of the top induction heads (L15h7, L11h1, L23h5) reduces loop-continuation logprob; apply edit
import shutil
def set_heads(scales):  # scales: dict {(layer,head): factor}; applies relative to ORIGINAL o_proj
    bylayer=collections.defaultdict(dict)
    for (l,h),f in scales.items(): bylayer[l][h]=f
    for l,hs in bylayer.items():
        name=f'model.language_model.layers.{l}.self_attn.o_proj.weight'
        Wt=load_original(name).clone()
        for h,f in hs.items(): Wt[:,h*256:(h+1)*256]*=f
        save_edit(name,Wt)
def clear_edits():
    for n in list(edited()): drop_edit(n)
clear_edits()
set_heads({(15,7):0.0,(11,1):0.0,(23,5):0.0})
print(edited())
```