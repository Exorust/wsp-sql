```python
# What does the model want right after SELECT? top-5 predictions at q_sel (for the first SELECT token), per gold kind
for i in range(36):
    q=dd.q_sel[i]; tops=[(tok.decode([tk12[i,q-1,j]]),round(float(tkl12[i,q-1,j]),2)) for j in range(6)]
    print(i, dd.kind[i], 'gold:',repr(dd.gold_after_select[i]), 'top:',tops)
```