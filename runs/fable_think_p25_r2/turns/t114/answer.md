```python
# Check fwd_3 (orig) vs fwd_4 (edit: zero L11h1,L15h7,L23h5) at bullet-end decision positions: did logP(NLNL)-logP(NL) change?
r3=json.load(open(f'{W}/tf3_req.json')); print(r3.keys(), len(r3.get('texts',r3.get('chats',[]))))
tk3=np.load(f'{W}/fwd_3/topk_ids.npy'); tl3=np.load(f'{W}/fwd_3/topk_logprobs.npy'); tk4=np.load(f'{W}/fwd_4/topk_ids.npy'); tl4=np.load(f'{W}/fwd_4/topk_logprobs.npy')
print(tk3.shape, tk4.shape)
def lpdiff(tkx,tlx,n,i):
    # logP(NLNL)-logP(NL) predicted at position i (for token i+1); missing from topk -> use -20
    d={int(t):float(l) for t,l in zip(tkx[n,i],tlx[n,i])}
    return d.get(271,-20.0)-d.get(198,-20.0), d.get(271,-20.0), d.get(198,-20.0)
texts3=r3['texts'] if 'texts' in r3 else None
for n in range(6):
    idsn=tok.encode(texts3[n]).ids
    dp=decision_positions(idsn)
    rows=[]
    for (i,nxt,line) in dp[-8:]:
        a=lpdiff(tk3,tl3,n,i); b=lpdiff(tk4,tl4,n,i)
        rows.append(f'{i}:{a[0]:.2f}->{b[0]:.2f}')
    print(n, len(idsn), ' '.join(rows))
```