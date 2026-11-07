```python
# Logit-lens: where does the </think>-vs-indent evidence arise? project hidden states onto d=(E[</think>]-E['   '])*normw at exit vs non-exit newline positions
sp3 = ex[1]; print("sp3 id", sp3, repr(tokstr(sp3)))
d = (E[TT]-E[sp3])*normw
H = {L: np.load(D7+f"/hidden_L{L}.npy") for L in [8,12,16,20,22,23]}
def proj(i,p,L):
    h = torch.from_numpy(H[L][i,p].astype(np.float32)); return float((h@d)/ (H[23][i,p].astype(np.float32)**2).mean()**0.5)
# positions: token at p-1 is '\n' (single) and we evaluate prediction for p; use p-1 index for hidden (prediction made at token p-1)
exit_p = pexit-1   # hidden at the '\n' token predicting </think>
cmp = [p-1 for p in range(1,pexit) if ids[p-1]==NL and ids[p]==sp3]
print("n cmp", len(cmp))
for L in [8,12,16,20,22,23]:
    ex_v = proj(0,exit_p,L); cm = [proj(0,q,L) for q in cmp]
    print(L, f"exit {ex_v:.2f} | cmp mean {np.mean(cm):.2f} sd {np.std(cm):.2f} max {np.max(cm):.2f}")
# actual logit diff check from topk: lp(</think>) - lp('   ') at exit
print("actual lp diff at exit:", lp7[0,pexit] - lp_of(0,pexit,sp3))
```