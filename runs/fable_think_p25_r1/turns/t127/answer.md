```python
# Fix indexing: topk[i,j] predicts token j+1. Re-check distribution right before </think>, and p(</think>) in loop texts at line starts
def dist_before(i,j,k=8):
    return [(tok.decode([a]),round(float(b),2)) for a,b in zip(tk[i,j-1,:k],tlp[i,j-1,:k])]
for i in [0,4,5]:
    ids=enc[i]
    for j in [jj for jj,x in enumerate(ids) if x==th_id]:
        print(i,j,'lp=%.2f'%lp[i,j], dist_before(i,j))
# In loop texts, for each '\n' token followed by indentation, see if </think> appears in top-50 and its lp
def rank_of(i,j,tid):
    row=tk[i,j-1]; w=np.where(row==tid)[0]
    return (int(w[0]), float(tlp[i,j-1,w[0]])) if len(w) else None
for i in [1,2,3]:
    ids=enc[i]
    nl=[j for j,x in enumerate(ids) if x==198 and j>700]
    rs=[rank_of(i,j+1,th_id) for j in nl]
    got=[r for r in rs if r]
    print(i, 'n newlines',len(nl),'</think> in top50 at', len(got), 'best lp', max([r[1] for r in got]) if got else None)
```