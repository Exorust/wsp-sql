```python
# Dose-response: set L16 col 3 to 1.6x the current steering (25x v16) and run on gen_16's exact ids
Wd=load_original('model.language_model.layers.16.mlp.down_proj.weight').clone()
Wd[:,3]=torch.tensor(c3*1.6)
save_edit('model.language_model.layers.16.mlp.down_proj.weight', Wd)
print(edited(), load('model.language_model.layers.16.mlp.down_proj.weight')[:,3].norm().item())
req={"type":"generate","model":"edited","problems":[r['id'] for r in rows],"max_tokens":2048}
json.dump(req,open(os.path.join(W,'gen18_req.json'),'w'))
print(json.dumps(req)[:3000])
```