```python
print(g.mean().item(), g.std().item(), g.min().item(), g.max().item())
d2=((E[271]-E[198])*(1+g)).numpy().astype(np.float32)
rows2=[]
for i in range(12):
    for p in range(tf5_meta[i]['pl'], L5[i]-1):
        a=np.where(tk5[i,p]==271)[0]; b=np.where(tk5[i,p]==198)[0]
        if len(a) and len(b):
            h=H[24][i,p].astype(np.float32); rms=np.sqrt((h**2).mean()+1e-6)
            rows2.append(((h@d2)/rms, tp5[i,p][a[0]]-tp5[i,p][b[0]]))
rows2=np.array(rows2); print(np.corrcoef(rows2[:,0],rows2[:,1])[0,1], np.polyfit(rows2[:,0],rows2[:,1],1))
```