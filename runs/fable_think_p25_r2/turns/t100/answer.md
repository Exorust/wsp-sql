```python
# Determine alignment between topk arrays and token ids
for off in [-1,0,1,2]:
    hits=np.mean([tk[0,i+off,0]==ids[i] for i in range(200,420) if 0<=i+off<424])
    print(off, round(hits,3))
```