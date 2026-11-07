```python
# L23n580 activation at each in-think '\n\n' position per text (is it a '3'-specific anti-digit neuron, active regardless of context?)
a580=M[23][:,:,580].astype(np.float32)
for i in range(6):
    ids=enc[i]; st=ids.index(tok.encode('<think>').ids[0])
    pos=[j for j,x in enumerate(ids) if x==271 and j>st]
    print(i, [(j, tok.decode(ids[j+1:j+2]).strip()[:3] or 'ws', round(float(a580[i,j]),1)) for j in pos][:14])
```