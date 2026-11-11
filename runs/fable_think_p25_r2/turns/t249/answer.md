```python
# Scan fwd_12 mlp acts (L12-20) for neurons that fire specifically at the first 'SELECT' token of the SQL (decision position)
selpos=[STARTS[i] for i in range(36)]
print([S(TOKS[i][selpos[i]]) for i in range(5)])
best={}
for L in range(12,21):
    A=np.load(os.path.join(F12,f'mlp_down_in_L{L}.npy')).astype(np.float32)
    acts_sel=np.array([A[i,selpos[i]] for i in range(36)])        # [36,3584]
    other=np.ones((36,330),bool)
    for i in range(36): other[i,selpos[i]]=False; other[i,lens12[i]:]=False
    A_other=A[other]                                                 # [n_other,3584]
    m_sel=acts_sel.mean(0); mn_sel=np.abs(acts_sel).min(0); sign_ok=(np.sign(acts_sel)==np.sign(m_sel)[None]).all(0)
    mx_other=np.abs(A_other).max(0); q99=np.quantile(np.abs(A_other),0.999,axis=0)
    score=np.where(sign_ok,mn_sel,0)/(q99+0.02)
    top=np.argsort(-score)[:4]
    best[L]=[(int(n),round(float(m_sel[n]),2),round(float(mn_sel[n]),2),round(float(q99[n]),2),round(float(mx_other[n]),2)) for n in top]
    print('L',L,'(neuron, meanSEL, min|SEL|, q99.9|other|, max|other|):',best[L])
```