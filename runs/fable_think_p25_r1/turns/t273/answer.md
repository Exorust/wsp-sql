```python
# Hypothesis: at the trigger ('<think>\n'), the original model gives '\n' a non-trivial probability (native no-think format would be '<think>\n\n</think>'); check fwd_4 top-k at the trigger.
tk4=np.load(W+'/fwd_4/topk_ids.npy'); tkl4=np.load(W+'/fwd_4/topk_logprobs.npy'); print(tk4.shape)
NL=tok.encode('\n').ids; NL2=tok.encode('\n\n').ids; print('ids',NL,NL2,END)
for k in range(0,40,8):
    ids=tok.encode(tx4[k]).ids; a=[i for i in range(len(ids)) if tok.decode(ids[max(0,i-1):i+1])=='<think>\n']
    if not a: continue
    a=a[0]; top=[(tok.decode([int(x)])[:10],round(float(l),2)) for x,l in zip(tk4[k,a],tkl4[k,a])]
    print(k,a,top[:8])
```