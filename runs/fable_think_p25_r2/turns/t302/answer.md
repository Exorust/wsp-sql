```python
# L16 neuron 3 activation stats (fwd_12 edited run, 36 gold chats): is it a constant-sign 'bias' neuron, in prompt and in SQL?
m16=np.load(os.path.join(W,'fwd_12','mlp_down_in_L16.npy'), mmap_mode='r')
lp12=np.load(os.path.join(W,'fwd_12','token_logprobs.npy')); mask=~np.isnan(lp12); mask[:,0]=True
a=np.asarray(m16[:,:,3]).astype(np.float32)
print('shape',a.shape,'mean',a[mask].mean().round(3),'std',a[mask].std().round(3),'min',a[mask].min().round(3),'max',a[mask].max().round(3),'frac<0',(a[mask]<0).mean().round(3))
# per-text: prompt region vs answer region (approx: last 40 valid tokens as answer)
L=mask.sum(1)
pr=[a[i,5:L[i]-45].mean() for i in range(len(L))]; an=[a[i,L[i]-40:L[i]].mean() for i in range(len(L))]
print('prompt-region mean',np.mean(pr).round(3),'answer-region mean',np.mean(an).round(3))
# effective steering: act * 15.6 * |v16| relative to residual norm at L16
h16=np.load(os.path.join(W,'fwd_12','hidden_L16.npy'), mmap_mode='r')
rn=np.linalg.norm(np.asarray(h16[0,5:L[0]]).astype(np.float32),axis=1)
print('resid norm L16 median',np.median(rn).round(2),'| steering vector norm (act -0.3)',(0.3*np.linalg.norm(c3)).round(2))
# how other neurons compare: fraction of neurons with |mean|/std > 3 (constant-like)
allm=np.asarray(m16[0,5:L[0]]).astype(np.float32); z=np.abs(allm.mean(0))/(allm.std(0)+1e-6)
print('top constant-like neurons at L16 (text0):',np.argsort(-z)[:8].tolist(), np.sort(z)[::-1][:8].round(1).tolist())
```