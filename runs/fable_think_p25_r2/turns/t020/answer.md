```python
# Hypothesis: gen_1_acts holds residual means for some layers; check what was saved
A=W+'/gen_1_acts'
print(os.listdir(A))
idx=json.load(open(A+'/index.json'))
print({k:(v if not isinstance(v,list) else (len(v), v[:3])) for k,v in idx.items()})
for f in os.listdir(A):
    if f.endswith('.npy'):
        a=np.load(A+'/'+f, mmap_mode='r'); print(f,a.shape,a.dtype)
```