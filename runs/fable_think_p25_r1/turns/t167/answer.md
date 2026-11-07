```python
# Find in fwd_7 texts the position where </think> is predicted; check its logprob and topk ranks of </think> elsewhere
import numpy as np
req7 = json.load(open(f"{W}/req7.json"))
texts7 = req7["texts"]
print([len(t) for t in texts7], ['</think>' in t for t in texts7])
TH = tok.encode("</think>").ids; print("think-close ids", TH, tok.encode("<think>").ids)
lp7 = np.load(f"{W}/fwd_7/token_logprobs.npy"); tk7 = np.load(f"{W}/fwd_7/topk_ids.npy"); tkl7 = np.load(f"{W}/fwd_7/topk_logprobs.npy")
print(lp7.shape, tk7.shape)
ids0 = tok.encode(texts7[0]).ids
print(len(ids0))
pos = [i for i,x in enumerate(ids0) if x==TH[0]]
print("</think> positions in text0:", pos)
for p in pos:
    print("context:", repr(tok.decode(ids0[p-12:p+6])), "lp of </think>:", lp7[0,p])
    print(" topk at that step:", [(tok.decode([int(i)]), round(float(l),2)) for i,l in zip(tk7[0,p], tkl7[0,p])][:8])
```