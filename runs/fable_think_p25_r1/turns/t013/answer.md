```python
print(idx['layers'], idx['shape_note'])
print(idx['samples'][:2])
A=np.load(f"{WORK}/gen_1_acts/resid_answer_mean.npy"); print(A.shape, A.dtype)
```