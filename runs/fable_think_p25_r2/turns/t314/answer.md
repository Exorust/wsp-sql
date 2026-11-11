```python
# Paired stats on set C and combined with set B; restore L16 edit; update notes
rows19=[json.loads(l) for l in open(os.path.join(W,'gen_19.jsonl'))]; rows20=[json.loads(l) for l in open(os.path.join(W,'gen_20.jsonl'))]
r19={r['id']:r for r in rows19}; r20={r['id']:r for r in rows20}
cC=[i for i in r19 if i in r20]
dC=np.array([float(r19[i]['cls']=='correct')-float(r20[i]['cls']=='correct') for i in cC])
dB=np.array([float(r16[i]['cls']=='correct')-float(r17[i]['cls']=='correct') for i in common])
print('setC n',len(dC),'diff',dC.mean().round(3),'se',(dC.std()/np.sqrt(len(dC))).round(3),'w->r',int((dC>0).sum()),'r->w',int((dC<0).sum()))
dd=np.concatenate([dB,dC]); print('combined n',len(dd),'diff',dd.mean().round(3),'se',(dd.std()/np.sqrt(len(dd))).round(3),'z',(dd.mean()/(dd.std()/np.sqrt(len(dd)))).round(2))
Wd=load_original('model.language_model.layers.16.mlp.down_proj.weight').clone(); Wd[:,3]=torch.tensor(c3); save_edit('model.language_model.layers.16.mlp.down_proj.weight', Wd); print(edited())
with open(os.path.join(W,'notes.md'),'a') as f:
    f.write(f"- setC (128 fresh ids, work/setC.json): gen_19 L18+L16 = 33.6%, gen_20 L18-only = 27.3%; paired diff +{dC.mean()*100:.1f} (se {dC.std()/np.sqrt(len(dC))*100:.1f}). Combined B+C n={len(dd)}: +{dd.mean()*100:.1f} se {dd.std()/np.sqrt(len(dd))*100:.1f}. L16 steer KEPT (x1.0). Current edited = best_1.\n")
```