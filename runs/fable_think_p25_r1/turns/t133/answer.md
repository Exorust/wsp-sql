```python
# Hypothesis: hidden_L23 = residual BEFORE layer 23; final = h23 + attn23 + mlp23. Check reconstruction with mlp23 added.
Wd23=load_original('model.language_model.layers.23.mlp.down_proj.weight'); print(Wd23.shape)
m23=np.load(F+'mlp_down_in_L23.npy'); print(m23.shape)
def logits_from(h, ids_list):
    h=torch.tensor(h.astype(np.float32)) if isinstance(h,np.ndarray) else h
    hn=h/torch.sqrt((h*h).mean()+eps)*nw
    return (E[ids_list]@hn).numpy()
for (i,j,alt) in [(2,811,id_3),(2,1071,id_4),(1,1067,id_3),(3,470,id_3)]:
    h=torch.tensor(h23[i,j].astype(np.float32)); mo=Wd23@torch.tensor(m23[i,j].astype(np.float32))
    a=logits_from(h,[id_ind,alt]); b=logits_from(h+mo,[id_ind,alt])
    print(i,j,'h only %.2f'%(a[0]-a[1]),' h+mlp23 %.2f'%(b[0]-b[1]),' true %.2f'%(tlp[i,j,0]-tlp[i,j,1] if tk[i,j,0]==id_ind else tlp[i,j,1]-tlp[i,j,0]), 'mlp23 norm %.2f h norm %.2f'%(mo.norm(),h.norm()))
```