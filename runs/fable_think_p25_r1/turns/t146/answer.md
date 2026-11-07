```python
# Do the digit-suppressor neurons fire wherever their digit is predicted (incl. SQL numbers), or only at section boundaries?
fam={580:3,598:5,557:1,250:0,564:4,669:6,485:2,639:7,380:2}
for n,d in fam.items():
    a=M[23][:,:,n].astype(np.float32)
    recs=[]
    for i in range(6):
        ids=enc[i]
        for j in range(1,len(ids)-1):
            if ids[j+1]==dig[d]:
                recs.append((i,j,ids[j],round(float(a[i,j]),1)))
    # split by previous token type
    at_nlnl=[r for r in recs if r[2]==271]; other=[r for r in recs if r[2]!=271]
    print(f'n{n} (digit {d}): next-token-is-digit positions: at nlnl {len(at_nlnl)} acts {[r[3] for r in at_nlnl][:6]} | elsewhere {len(other)} acts {[r[3] for r in other][:10]} ctx {[repr(tok.decode(enc[r[0]][r[1]-3:r[1]+2])) for r in other[:3]]}')
```