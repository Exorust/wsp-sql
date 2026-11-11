```python
# Load fwd_5 outputs; verify DLA setup: logit(\n\n)-logit(\n) from final hidden vs topk logprob difference
F=W+'/fwd_5'
m5=json.load(open(F+'/meta.json')); L5=m5['lengths']
lp5=np.load(F+'/token_logprobs.npy'); tk5=np.load(F+'/topk_ids.npy'); tp5=np.load(F+'/topk_logprobs.npy')
H={l:np.load(F+f'/hidden_L{l}.npy') for l in range(25)}
print(H[24].shape, H[24].dtype)
E=load('model.language_model.embed_tokens.weight'); g=load('model.language_model.norm.weight')
print(E.shape, g.shape)
d=((E[271]-E[198])*g).numpy().astype(np.float32)
ids5=[tok.encode(t).ids for t in tf5_texts[:12]]
print([len(x) for x in ids5]==L5)
# check: at a few positions, compare
rows=[]
for i in range(12):
    for p in range(tf5_meta[i]['pl'], L5[i]-1):
        a=np.where(tk5[i,p]==271)[0]; b=np.where(tk5[i,p]==198)[0]
        if len(a) and len(b):
            h=H[24][i,p].astype(np.float32); rms=np.sqrt((h**2).mean())+1e-6
            pred=(h@d)/rms
            rows.append((pred, tp5[i,p][a[0]]-tp5[i,p][b[0]]))
rows=np.array(rows); print(len(rows), np.corrcoef(rows[:,0],rows[:,1])[0,1], rows[:5])
```