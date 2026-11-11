```python
# Check norm weight conventions (values near 0 => (1+w) convention; near 1 => standard) and D18 neuron sanity
for n in ['model.language_model.layers.14.input_layernorm.weight','model.language_model.layers.14.post_attention_layernorm.weight','model.language_model.norm.weight']:
    w=load(n); print(n.split('.')[-2], 'mean %.3f std %.3f min %.3f max %.3f'%(w.mean(),w.std(),w.min(),w.max()))
print([n for n in NAMES if 'layers.14.' in n])
```