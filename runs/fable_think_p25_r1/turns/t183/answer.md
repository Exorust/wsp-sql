```python
# Compute the </think> write direction and per-neuron scaling needed; check overlap with competitor unembeddings
uTC = gN*E[ID_TC]; nrm = float(uTC.norm()); u = uTC/nrm
print("|gN*E[TC]| =", round(nrm,3))
comp = {'Thinking':ID_THINKING,'The':ID_THE,'Okay':ID_OKAY,'Let':ID_LET,'\\n\\n':tok.encode("\n\n").ids[0],'   ':ID_IND, 'SELECT':tok.encode("SELECT").ids[0], 'sql-fence': tok.encode(FENCE+"sql").ids[0]}
print({k: round(float(u @ (gN*E[v]))/nrm,3) for k,v in comp.items()})  # cosine-ish: relative logit gain of competitor per unit gain of TC
# per-unit-alpha logit gain of TC at first pos for candidate neurons: act*alpha*nrm/rms
rms_first = np.mean([float(np.sqrt((H[23][n,first_pos[n]].astype(np.float32)**2).mean())) for n in range(6)])
print("rms at first pos", round(rms_first,3))
for (l,j) in [(18,628),(20,1235),(17,537),(19,2424),(17,2138),(20,1981),(17,1533),(18,2763),(19,2800)]:
    a = np.mean([float(Mall[l][n,first_pos[n],j]) for n in range(6)])
    print((l,j), "act", round(a,2), "Δlogit per alpha =", round(a*nrm/rms_first,2), " col norm", round(float(Wd_all[l][:,j].norm()),3))
```