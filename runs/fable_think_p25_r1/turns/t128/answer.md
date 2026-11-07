```python
# Loop statistics from setA (onset/period in tokens) and a sample of loop content
A=json.load(open(W+'/setA.json'))
print(type(A), len(A), A[0].keys() if isinstance(A[0],dict) else None)
on=np.array([a['onset'] for a in A]); per=np.array([a['period'] for a in A])
print('onset quantiles', np.percentile(on,[10,25,50,75,90]).astype(int))
print('period quantiles', np.percentile(per,[10,25,50,75,90]).astype(int))
# show one loop period from text 2 of fwd_7
ids=enc[2]
print(repr(tok.decode(ids[900:1150])))
```