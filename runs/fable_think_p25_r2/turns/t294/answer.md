```python
# Reconstruct passes 13-16: read request files, done files and gen_16 results
for f in ['gen16_req.json','tf13_meta.json','tf14_req.json','fwd_13.done.json','fwd_14.done.json','fwd_15.done.json','fwd_16.done.json']:
    p=os.path.join(W,f)
    try:
        s=open(p).read()
        print('==',f,len(s)); print(s[:1200])
    except Exception as e: print(f,e)
for d in ['fwd_13','fwd_14','fwd_15']:
    print(d, os.listdir(os.path.join(W,d)))
    try: print(open(os.path.join(W,d,'meta.json')).read()[:600])
    except Exception as e: print(e)
v16=np.load(os.path.join(W,'v16.npy')); print('v16',v16.shape, np.linalg.norm(v16))
```