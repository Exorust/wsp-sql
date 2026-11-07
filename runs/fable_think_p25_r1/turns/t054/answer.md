```python
# Reconstruct the fwd_2 token sequences and verify alignment with top-1 predictions
import numpy as np
def render_chat(user, assistant, thinking_inside=False):
    s = "<|im_start|>user\n" + user + "<|im_end|>\n<|im_start|>assistant\n<think>\n"
    if thinking_inside:
        return s + assistant
    return s + "\n</think>\n\n" + assistant + "<|im_end|>\n"
F2 = W+"/fwd_2/"
lp = np.load(F2+"token_logprobs.npy"); tk = np.load(F2+"topk_ids.npy"); tklp = np.load(F2+"topk_logprobs.npy")
print(lp.shape, tk.shape)
seqs = []
for ci, c in enumerate(req2['chats']):
    s = render_chat(c[0]['content'], c[1]['content'])
    ids = tok.encode(s).ids
    print(ci, len(ids), "expected", json.load(open(F2+"meta.json"))['lengths'][ci])
    seqs.append(ids)
# check alignment: top1 at position t-1 vs actual id at t
for ci, ids in enumerate(seqs):
    n = min(len(ids), tk.shape[1])
    pred = tk[ci,:n-1,0]; act = np.array(ids[1:n])
    print(ci, "top1 match rate", (pred==act).mean(), "last 300:", (pred[-300:]==act[-300:]).mean())
```