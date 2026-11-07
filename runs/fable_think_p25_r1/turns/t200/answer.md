```python
# Where else does L20n1235 fire (outside the first position)? And the other three detectors' max-rest contexts
for (l,j) in [(20,1235),(18,628),(17,537),(19,2424)]:
    a = Mall[l][:, :, j].astype(np.float32)
    flat = [(abs(a[n,q]), n, q) for n in range(6) for q in range(1,lens7[n]) if q!=first_pos[n]]
    flat.sort(reverse=True)
    print(f"L{l}n{j} top non-first |act|:")
    for v,n,q in flat[:4]:
        print("   ", round(float(a[n,q]),2), repr(tok.decode(ids7[n][max(0,q-8):q+1]))[-60:], "-> next:", repr(tok.decode([ids7[n][q+1]])) if q+1<lens7[n] else "")
```