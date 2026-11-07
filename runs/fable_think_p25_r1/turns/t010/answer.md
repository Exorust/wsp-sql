```python
# Characterize loop onset per text: token index where repetition begins and the period (in tokens)
def find_loop(ids, minper=3, maxper=400):
    # find earliest i such that ids[i:i+3*p] is periodic with some period p, scanning i
    n=len(ids)
    arr=np.array(ids)
    for i in range(0, n-100, 8):
        seg=arr[i:i+1200] if i+1200<=n else arr[i:]
        for p in range(minper, min(maxper, len(seg)//3)):
            if np.array_equal(seg[:p], seg[p:2*p]) and np.array_equal(seg[:p], seg[2*p:3*p]):
                # refine i backwards
                j=i
                while j>0 and j+2*p<n and arr[j-1]==arr[j-1+p]: j-=1
                return j, p
    return None, None
onsets=[]
for g in gens:
    ids=tok.encode(g['text']).ids
    o,p=find_loop(ids)
    onsets.append((g['id'],o,p,len(ids)))
ons=[o for _,o,p,_ in onsets if o is not None]
pers=[p for _,o,p,_ in onsets if o is not None]
print("found loops:", len(ons), "/", len(onsets))
print("onset token percentiles:", np.percentile(ons,[10,25,50,75,90]))
print("period percentiles:", np.percentile(pers,[10,25,50,75,90]))
```