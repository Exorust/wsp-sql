```python
# Same, avoiding literal triple backticks in code
FENCE='`'*3
safe=['   ','    ','  ',' ','\n','\n\n','*',' *','**','1','2','3','4','5','6','7','8','9','</think>',FENCE,'SELECT','FROM','WHERE',' Wait','Wait','Okay','The',' The',' So','So','Final','Let','I','-','#','##']
sids=[tok.encode(s).ids for s in safe]; sids=[(s,i[0]) for s,i in zip(safe,sids) if len(i)==1]
ES=torch.stack([E[i] for s,i in sids])*nw
def promote(L,n,sign=1):
    v=Wd[L][:,n]*sign
    sc=(ES@v).numpy()
    order=np.argsort(-sc)
    return [(sids[k][0],round(float(sc[k]),2)) for k in order[:6]], [(sids[k][0],round(float(sc[k]),2)) for k in order[-4:]]
for (L,n,sg) in [(23,932,+1),(23,385,-1),(22,1267,-1),(18,128,-1),(20,669,+1),(22,796,-1),(23,580,-1),(21,206,+1),(20,168,+1),(22,817,-1),(23,1669,+1),(23,879,+1),(23,935,+1)]:
    p,q=promote(L,n,sg); print(f'L{L}n{n} (sign {sg:+d}): promotes',p,' demotes',q)
```