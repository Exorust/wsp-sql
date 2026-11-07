```python
# Check sign/calibration behaviour of top bullet-end neurons: activation at points where '\n\n' was chosen vs '\n' chosen (soft vs hard)
cands=[(23,1669),(23,195),(23,9),(23,985),(20,190),(21,371),(21,0),(21,761),(22,817),(23,879),(23,935)]
de2=de.copy()
for (L,n) in cands:
    de2[f'L{L}n{n}']=[float(M[L][r.i,r.j-1,n]) for r in de.itertuples()]
    de2[f'c{L}_{n}']=[float(neuron_contrib(L,r.i,r.j-1,198,271)[n]) for r in de.itertuples()]
grp=de2.assign(kind=np.where(de2.chosen=='nlnl','nlnl',np.where(de2.margin<3,'nl_soft','nl_hard'))).groupby('kind')
cols=[f'L{L}n{n}' for L,n in cands]+[f'c{L}_{n}' for L,n in cands]
print(grp.size()); print(grp[cols].mean().round(2).T.to_string())
```