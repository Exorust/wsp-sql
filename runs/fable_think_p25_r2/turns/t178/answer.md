```python
# How selective is L18 neuron 2800? Check its down_proj input activation across positions in fwd_9 (T1..T4 texts) and fwd_8 (long loop texts)
a9=np.load(f'{W}/fwd_9/mlp_down_in_L18.npy')[:,:,2800].astype(np.float32)  # [N,T]
kinds9=json.load(open(f'{W}/tf9_meta.json'))['kinds']
for i,t in enumerate(texts9):
    ids,pos=positions(t); n=len(ids); p=pos[0]
    a=a9[i,:n]
    top=np.argsort(-np.abs(a))[:5]
    print(i,kinds9[i],'n',n,'p',p,'act@p-1..p+1',np.round(a[p-1:p+2],2),'| max|act| pos',top.tolist(),np.round(a[top],2),'| mean|act| %.3f'%np.abs(a).mean())
a8=np.load(f'{W}/fwd_8/mlp_down_in_L18.npy')[:,:,2800].astype(np.float32)
print('fwd_8 shapes',a8.shape)
for i in range(a8.shape[0]):
    a=a8[i]; n=(np.load(f'{W}/fwd_8/token_logprobs.npy')[i]==np.load(f'{W}/fwd_8/token_logprobs.npy')[i]).sum()+1
    a=a[:n]; top=np.argsort(-np.abs(a))[:8]
    print(i,'n',n,'max|act| pos',top.tolist(),np.round(a[top],2),'mean|act| %.3f'%np.abs(a).mean(), 'frac |act|>0.5: %.3f'%(np.abs(a)>0.5).mean())
```