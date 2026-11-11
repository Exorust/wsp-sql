```python
# Where does </think> (248069) get probability? Scan fwd_3 topk over the 6 loop texts and 16 gold chats
d3=os.path.join(W,'fwd_3')
lp3=np.load(os.path.join(d3,'token_logprobs.npy')); tk3=np.load(os.path.join(d3,'topk_ids.npy')); tl3=np.load(os.path.join(d3,'topk_logprobs.npy'))
print(lp3.shape, tk3.shape)
req3=json.load(open(os.path.join(W,'tf3_req.json')))
texts3=req3.get('texts'); print(len(texts3))
ids3=[tok.encode(t).ids for t in texts3]
print([len(x) for x in ids3][:8], m3['lengths'][:8])
TH=248069
best=collections.Counter(); 
for i in range(len(texts3)):
    n=len(ids3[i])
    for p in range(1,n):
        # topk at position p predicts token p (ids3[i][p]) given prefix; find </think> in topk
        w=np.where(tk3[i,p]==TH)[0]
        if len(w):
            prev=ids3[i][p-1]
            best[(i, tok.decode([prev])[:12], round(float(tl3[i,p,w[0]]),1))]+=1
# print the top entries sorted by logprob
items=sorted(best.items(), key=lambda kv:-kv[0][2])[:25]
for k,v in items: print(k,v)
```