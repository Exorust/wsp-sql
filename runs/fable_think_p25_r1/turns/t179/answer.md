```python
# At the first thinking position: rank/logprob of </think>, and DLA of (</think> - 'Thinking') margin by component
for n in range(6):
    q = first_pos[n]
    row = list(tk7[n,q]); 
    r = row.index(ID_TC) if ID_TC in row else None
    print(n, "rank of </think> in top50:", r, "lp:", (round(float(tkl7[n,q,r]),2) if r is not None else None), "min lp in top50:", round(float(tkl7[n,q,-1]),2))
d2 = gN*(E[ID_TC]-E[ID_THINKING])
def attrib_dir(n, q, dv):
    h23 = torch.tensor(H[23][n,q].astype(np.float32)); rms = h23.pow(2).mean().sqrt()
    h20 = torch.tensor(H[20][n,q].astype(np.float32)); h22 = torch.tensor(H[22][n,q].astype(np.float32))
    mlp = {l: Wd_all[l] @ torch.tensor(Mall[l][n,q].astype(np.float32)) for l in [21,22,23]}
    parts = {"h20": (h20@dv)/rms, "mlp21": (mlp[21]@dv)/rms, "mlp22": (mlp[22]@dv)/rms, "attn21+22": ((h22-h20-mlp[21]-mlp[22])@dv)/rms,
             "mlp23": (mlp[23]@dv)/rms, "attn23": ((h23-h22-mlp[23])@dv)/rms}
    return round(float((h23@dv)/rms),2), {k: round(float(v),2) for k,v in parts.items()}
for n in range(6):
    print(n, attrib_dir(n, first_pos[n], d2))
```