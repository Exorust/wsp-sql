```python
# Hypothesis: hidden_L24 is post-final-norm. Verify: rms(h23+attn+mlp)*(1+wn) == H24
wnn=wn.numpy()
hf=H23_6[n,:T].astype(np.float32)+rec+M23_6[n,:T].astype(np.float32)@Wd23.T
normed=rms(hf)*(1+wnn)
err=np.linalg.norm(normed-H24_6[n,:T].astype(np.float32),axis=1)/np.linalg.norm(H24_6[n,:T].astype(np.float32),axis=1)
print('rel err of final-norm reconstruction: median', np.median(err).round(4), 'max', err.max().round(4))
# Alternative with w convention (no 1+)
normed2=rms(hf)*wnn; err2=np.linalg.norm(normed2-H24_6[n,:T].astype(np.float32),axis=1)/np.linalg.norm(H24_6[n,:T].astype(np.float32),axis=1)
print('w-only convention err', np.median(err2).round(4))
```