```python
# Hypothesis: v3 direction promotes 'Okay' (i.e., start a short think) rather than </think>
for s in ['Okay',' Okay','</think>','Thinking','First','We','Let','To']:
    ids=tok.encode(s).ids
    if len(ids)==1:
        w=gN*E[ids[0]]; w=w/w.norm(); print(repr(s), round(float(da@w),3))
# maybe combination: a*u(</think>) + b*u(Okay)? solve least squares
A=torch.stack([ (gN*E[think_id[0]])/ (gN*E[think_id[0]]).norm(), (gN*E[31248])/(gN*E[31248]).norm()],1)
coef=torch.linalg.lstsq(A,da[:,None]).solution.squeeze(); res=(da-A@coef).norm()
print('coef',coef.tolist(),'resid',float(res))
```