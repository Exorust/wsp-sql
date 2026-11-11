```python
# Check constant-direction (bias proxy) in normalised MLP input at L14, dead-neuron candidates, and the direction v's composition
L=14
xpre,xn,A=mlp_inputs(L)
Xv=xn[valid]
mu_all=Xv.mean(0); b=mu_all/np.linalg.norm(mu_all)
pb=Xv@b; print('proj on mean dir: mean %.2f std %.2f min %.2f max %.2f'%(pb.mean(),pb.std(),pb.min(),pb.max()))
pbs=xn[isSEL]@b; print('  at SELECT: mean %.2f std %.2f'%(pbs.mean(),pbs.std()))
nrm=np.linalg.norm(Xv,axis=1); print('|xn| mean %.2f std %.2f'%(nrm.mean(),nrm.std()))
# dead neurons at L14
mx=np.abs(A[valid]).max(0); Wd=load(f'model.language_model.layers.{L}.mlp.down_proj.weight').numpy(); coln=np.linalg.norm(Wd,axis=0)
score=mx*coln; order=np.argsort(score)[:8]
print('least-used neurons (idx, max|act|, |col|):', [(int(n),round(float(mx[n]),3),round(float(coln[n]),3)) for n in order])
# direction v at L14 (SELECT diff) composition
v=dirs[14]['sel']; vu=v/np.linalg.norm(v)
top=np.argsort(-np.abs(vu))[:8]; print('v top dims', [(int(d),round(float(vu[d]),2)) for d in top], 'sum sq top8 %.2f'%(vu[top]**2).sum())
hid=H13[14].astype(np.float32); rr=np.sqrt((hid[:32][np.array([[True]*LEN13[a]+[False]*(304-LEN13[a]) for a in range(32)])]**2).mean(0))
print('resid rms per dim at those dims:', [round(float(rr[d]),2) for d in top], ' median rms %.3f'%np.median(rr))
```