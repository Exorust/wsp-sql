```python
# Hypothesis: the INSTR1-induced hidden-state shift over SQL tokens is a consistent direction across problems (steerable)
H={l:np.load(d+f'hidden_L{l}.npy') for l in [10,12,14,16,18]}
print({l:H[l].shape for l in H})
diffs={l:[] for l in H}; norms={l:[] for l in H}
for j in range(32):
    a0,b0,_=my_sql_span(T[j]); a1,b1,_=my_sql_span(T[32+j]); assert b0-a0==b1-a1
    for l in H:
        h0=H[l][j,a0:b0].astype(np.float32); h1=H[l][32+j,a1:b1].astype(np.float32)
        diffs[l].append((h1-h0).mean(0)); norms[l].append(np.linalg.norm(h0,axis=1).mean())
for l in H:
    D=np.array(diffs[l]); mu=D.mean(0); 
    cos=(D@mu)/(np.linalg.norm(D,axis=1)*np.linalg.norm(mu)+1e-6)
    print(f'L{l}: resid norm {np.mean(norms[l]):.2f}, mean diff norm {np.linalg.norm(mu):.3f}, per-problem diff norm {np.linalg.norm(D,axis=1).mean():.3f}, cos(problem diff, mean) {cos.mean():.2f} min {cos.min():.2f}')
```