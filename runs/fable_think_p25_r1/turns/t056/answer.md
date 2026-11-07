```python
# Analyze attention in the loop region of seq 0: per head, mass on induction target (t+1-p), on previous token, on the prompt, on earlier repeats
ids0 = seqs[0][:1340]; p0 = 61; onset0 = 789
layers_fa = [3,7,11,15,19,23]
A = {L: np.load(F2+f"attn_L{L}_text0.npy") for L in layers_fa}
print(A[3].shape, A[3].dtype)
T = 1340
rows_out = []
qpos = np.arange(onset0+p0, T-1)   # query positions well inside the loop
for L in layers_fa:
    a = A[L].astype(np.float32)  # [heads, T, T]
    for h in range(a.shape[0]):
        m = a[h][qpos]            # [nq, T]
        ind = np.array([m[i, q+1-p0] for i,q in enumerate(qpos)]).mean()      # induction: token after previous occurrence
        ind2 = np.array([m[i, q+1-2*p0] for i,q in enumerate(qpos)]).mean()   # two periods back
        same = np.array([m[i, q-p0] for i,q in enumerate(qpos)]).mean()       # previous occurrence of same token
        prev = np.array([m[i, q] for i,q in enumerate(qpos)]).mean()          # attends to current token (self)
        prompt = m[:, :245].sum(1).mean()
        first = m[:, 0].mean()
        rows_out.append((L,h,ind,ind2,same,prev,prompt,first))
import pandas as pd
df = pd.DataFrame(rows_out, columns=["L","h","ind(+1-p)","ind(+1-2p)","same(-p)","self","prompt","bos"])
print(df.round(3).to_string())
```