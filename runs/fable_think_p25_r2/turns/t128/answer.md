```python
# At every '\n\n' position in the thinking (predicting the next token): what are the top candidates and logP(</think>)?
F8=f'{W}/fwd_8'; tk8=np.load(f'{F8}/topk_ids.npy'); tl8=np.load(f'{F8}/topk_logprobs.npy'); lp8=np.load(f'{F8}/token_logprobs.npy')
texts8=[textA,textB]; ids8=[tok.encode(t).ids for t in texts8]; lens8=[len(i) for i in ids8]
print(lens8)
def show_pred(n,i,k=6):
    d=[(tok.decode([int(t)]).replace('\n','\\n'), round(float(l),2)) for t,l in zip(tk8[n,i][:k],tl8[n,i][:k])]
    dd={int(t):float(l) for t,l in zip(tk8[n,i],tl8[n,i])}
    return d, dd.get(248069, None)
for n in range(2):
    idsn=ids8[n]; st=[i for i,t in enumerate(idsn) if t==248068][0]
    print('== text',n)
    for i in range(st,lens8[n]):
        if idsn[i]==271:  # '\n\n' token: prediction for next token at index i
            ctx=tok.decode(idsn[i-8:i]).replace('\n','\\n')
            d,e=show_pred(n,i); print(f'{i:5d} [{ctx[-40:]}] -> {d}  </think>={e}')
```