```python
# Final: verify edited folder matches best_1 and write final notes
import filecmp
ed=os.path.join(W,'edited'); b1=os.path.join(W,'best_1')
print(sorted(os.listdir(ed))); print('match best_1:', all(np.array_equal(np.load(os.path.join(ed,f)),np.load(os.path.join(b1,f))) for f in os.listdir(ed)))
c16=load('model.language_model.layers.16.mlp.down_proj.weight'); c18=load('model.language_model.layers.18.mlp.down_proj.weight')
print('L16 col3 norm',c16[:,3].norm().item(),'L18 col2800 norm',c18[:,2800].norm().item(), 'other cols unchanged:', torch.equal(torch.cat([c16[:,:3],c16[:,4:]],1), torch.cat([load_original('model.language_model.layers.16.mlp.down_proj.weight')[:,:3],load_original('model.language_model.layers.16.mlp.down_proj.weight')[:,4:]],1)))
with open(os.path.join(W,'notes.md'),'a') as f:
    f.write("- gen_24 (both, 64 fresh ids setG, 8192 tok): original 1.6% vs edited 32.8%; paired +31.3 (se 5.8), 20 w->r, 0 r->w.\n  COMBINED final confirmation (128 fresh problems): original 0.8% -> edited 26.6% (+25.8 points, 33 w->r, 0 r->w).\n- SUBMITTED: work/edited = best_1 (L18 col 2800 skip-thinking neuron + L16 col 3 simplicity steer). 24/25 passes used.\n")
```