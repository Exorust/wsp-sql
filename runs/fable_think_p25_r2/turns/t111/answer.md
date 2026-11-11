```python
n=0;T=424
true=H24_6[n,:T].astype(np.float32)-H23_6[n,:T].astype(np.float32)-M23_6[n,:T].astype(np.float32)@Wd23.T
rec=HO[n].sum(0)
print('true norm', np.linalg.norm(true,axis=1)[100:105].round(1), 'rec norm', np.linalg.norm(rec,axis=1)[100:105].round(1))
cos=(rec*true).sum(1)/np.linalg.norm(rec,axis=1)/np.linalg.norm(true,axis=1); print('cos', np.round(cos[100:105],3), np.median(cos).round(3))
# attention pattern sanity: rows sum to 1?
print('row sums', A23[0][0,100:103,:].astype(np.float32).sum(1), 'first row', A23[0][0,0,:3])
# alternative gate split: gate first
x=rms(H23_6[n,:T].astype(np.float32))*(1+win); QG=(x@Wq.T).reshape(T,8,512)
print('mean |q part| vs |gate part|:', np.abs(QG[:,:,:256]).mean().round(3), np.abs(QG[:,:,256:]).mean().round(3))
```