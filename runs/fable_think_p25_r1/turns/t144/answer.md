```python
# For each section boundary, which neurons most oppose the upcoming digit? Look for digit-specific suppressor neurons
def top_opposers(i,j,d_id,k=4):
    res=[]
    for L in range(16,24):
        c=neuron_contrib(L,i,j,id_ind,d_id)
        for n in np.argsort(-c)[:k]: res.append((round(float(c[n]),2),f'L{L}n{n}'))
    return sorted(res,reverse=True)[:k]
for i in range(6):
    ids=enc[i]; st=ids.index(tok.encode('<think>').ids[0])
    for j in [j for j,x in enumerate(ids) if x==271 and j>st]:
        # top digit competitor in topk
        row=tk[i,j]; cands=[(float(tlp[i,j,r]),int(row[r])) for r in range(50) if int(row[r]) in digit_ids]
        if not cands: continue
        lpd,d=max(cands); 
        w=np.where(row==id_ind)[0]; lpi=float(tlp[i,j,w[0]]) if len(w) else -20
        if abs(lpi-lpd)<4:
            print(i,j,'digit',tok.decode([d]),'margin ind-dig %.2f'%(lpi-lpd), top_opposers(i,j,d))
```