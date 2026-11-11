```python
# Compare L14-steer gold lp (fwd_22, 12 texts) with base (fwd_13 sel) and L16 steers (fwd_14/15 restricted to sel)
lp22=np.load(os.path.join(W,'fwd_22','token_logprobs.npy'))
g22=np.array([np.nanmean(lp22[j,slice(*sqlpos(T[i],lp22[j]))]) for j,i in enumerate(sel)])
g14=np.array([np.nanmean(lp14[i,slice(*sqlpos(T[i],lp14[i]))]) for i in sel]); g15=np.array([np.nanmean(lp15[i,slice(*sqlpos(T[i],lp15[i]))]) for i in sel])
for nm,g in [('L16 A (fwd_14)',g14),('L16 B (fwd_15)',g15),('L14 steer (fwd_22)',g22),('INSTR1 in-context',i1)]:
    d=g-base; print(f'{nm}: gain {d.mean():+.4f} se {d.std()/np.sqrt(12):.4f}')
# also the lengths match? (sanity: same tokenization as fwd_13 base)
print('len check', [int(np.sum(~np.isnan(lp22[j])))+1 for j in range(3)], [int(np.sum(~np.isnan(lp13full[i])))+1 for i in sel[:3]])
```