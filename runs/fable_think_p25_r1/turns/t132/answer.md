```python
# Verify logit reconstruction from hidden_L23 (final residual) via final norm + tied embedding at a decision point
E=load_original('model.language_model.embed_tokens.weight'); nw=load_original('model.language_model.norm.weight')
print(E.shape, nw.shape)
h23=np.load(F+'hidden_L23.npy'); print(h23.shape)
eps=1e-6
def logits_at(i,j,ids_list):
    h=torch.tensor(h23[i,j].astype(np.float32))
    hn=h/torch.sqrt((h*h).mean()+eps)*nw
    return (E[ids_list]@hn).numpy(), float(torch.sqrt((h*h).mean()))
id_ind=262; id_3=tok.encode('3').ids[0]; id_4=tok.encode('4').ids[0]; print('3',id_3,'4',id_4)
for (i,j,alt) in [(2,811,id_3),(2,1071,id_4),(1,1067,id_3),(3,470,id_3)]:
    lg,rms=logits_at(i,j,[id_ind,alt])
    print(i,j,'logit(ind)-logit(digit)=%.2f'%(lg[0]-lg[1]), 'from topk: %.2f'%(tlp[i,j,0]-tlp[i,j,1]), dist_before(i,j+1,2), 'rms=%.1f'%rms)
```