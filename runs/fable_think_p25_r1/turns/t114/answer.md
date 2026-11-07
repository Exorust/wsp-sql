```python
# What competes at the post-"\n\n" positions after conclusion sentences? And profile neuron L22/796: vocab projection + activation pattern
for p in [1270, 1399, 1039, 1365, 1461]:
    print(p, repr(tok.decode(ids[p-6:p])), [(tokstr(ti7[0,p-1,k]), round(float(tl7[0,p-1,k]),1)) for k in range(8)])
v = E @ DP[22][:,796]  # (vocab,) effect of neuron 796 output on logits (unnormalized)
top = torch.topk(v, 12).indices; bot = torch.topk(-v, 12).indices
print("promoted ids:", [(int(i), repr(tokstr(i))) for i in top])
print("suppressed ids:", [(int(i), repr(tokstr(i))) for i in bot])
print("</think> score", float(v[TT]), "indent score", float(v[sp3]), "rank of </think> among suppressed:", int((v < v[TT]).sum()))
```