```python
# fwd_8: the two far-progressing texts. Where does </think> appear in topk, what competes?
d8=os.path.join(W,'fwd_8'); m8=json.load(open(os.path.join(d8,'meta.json')))
lp8=np.load(os.path.join(d8,'token_logprobs.npy')); tk8=np.load(os.path.join(d8,'topk_ids.npy')); tl8=np.load(os.path.join(d8,'topk_logprobs.npy'))
req8=json.load(open(os.path.join(W,'tf8_req.json'))); texts8=req8['texts']; ids8=[tok.encode(t).ids for t in texts8]
print(lp8.shape, [len(x) for x in ids8], m8['lengths'])
for i in range(2):
    ids=ids8[i]; n=len(ids)
    hits=[]
    for p in range(n-1):
        w=np.where(tk8[i,p]==TH)[0]
        if len(w): hits.append((p, float(tl8[i,p,w[0]]), tok.decode(ids[max(0,p-8):p+1]).replace('\n','|')[-60:], tok.decode([ids[p+1]]).replace('\n','|'), float(lp8[i,p+1])))
    hits.sort(key=lambda x:-x[1])
    print('text',i,'n hits',len(hits))
    for h in hits[:12]: print('  ', h[0], round(h[1],2), repr(h[2]), '-> actual', repr(h[3]), round(h[4],2))
```