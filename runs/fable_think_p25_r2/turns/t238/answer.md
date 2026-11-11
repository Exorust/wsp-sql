```python
# Find candidate 'carrier' neurons: active consistently on SQL tokens (assistant region) but ~0 in the prompt (fwd_12, layers 12-20)
lens12=[len(ids) for ids in IDS]
maskSQL=np.zeros((36,330),bool); maskPR=np.zeros((36,330),bool)
for i in range(36):
    maskSQL[i,STARTS[i]:lens12[i]-1]=True   # SQL tokens incl closing fence
    maskPR[i,5:STARTS[i]-8]=True            # prompt region (schema etc.)
cand={}
for L in range(12,21):
    f=os.path.join(F12,f'mlp_down_in_L{L}.npy')
    if not os.path.exists(f): continue
    A=np.load(f).astype(np.float32)
    sq=A[maskSQL]; pr=A[maskPR]
    m_sq=sq.mean(0); s_sq=sq.std(0); mn_sq=np.abs(sq).min(0); m_pr=np.abs(pr).mean(0); mx_pr=np.abs(pr).max(0)
    # score: large min |act| in SQL (same sign), small max |act| in prompt
    sign_ok=(np.sign(sq)==np.sign(m_sq)[None]).all(0)
    score=np.where(sign_ok, mn_sq, 0)/(mx_pr+0.05)
    top=np.argsort(-score)[:5]
    cand[L]=[(int(n), round(float(m_sq[n]),3), round(float(s_sq[n]),3), round(float(mn_sq[n]),3), round(float(m_pr[n]),3), round(float(mx_pr[n]),3)) for n in top]
    print('L',L, 'neuron, meanSQL, stdSQL, min|SQL|, mean|prompt|, max|prompt|:', cand[L][:3])
```