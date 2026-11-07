```python
# Analyze pass 7: where does </think> rank at paragraph boundaries? First the success text: p(</think>) at the actual exit and at earlier "\n\n" positions
D7 = W+"/fwd_7"
lp7=np.load(D7+"/token_logprobs.npy"); ti7=np.load(D7+"/topk_ids.npy"); tl7=np.load(D7+"/topk_logprobs.npy")
TT=248069
ids7=[tok.encode(t).ids for t in texts]
def lp_of(i,p,tid):
    # logprob of token tid predicted at position p (i.e., logits after token p-1): topk at p-1
    row=ti7[i,p-1]; m=np.where(row==tid)[0]
    return float(tl7[i,p-1,m[0]]) if len(m) else None
i=0; ids=ids7[0]
pexit=ids.index(TT); print("exit pos", pexit, "prev toks", [tokstr(x) for x in ids[pexit-4:pexit+1]])
print("lp(</think>) at exit:", lp7[0,pexit], "top5:", [(tokstr(ti7[0,pexit-1,k]), round(float(tl7[0,pexit-1,k]),2)) for k in range(5)])
# at all positions where the current token follows '\n' or '\n\n' in the thinking, what is lp(</think>)?
NL=ex[17]; NL2=tok.encode("\n\n").ids[0]; print("ids", NL, NL2)
rows=[]
for p in range(1,len(ids)):
    if ids[p-1] in (NL,NL2) and p<pexit:
        rows.append((p, tokstr(ids[p]), round(float(lp7[0,p]),2), lp_of(0,p,TT)))
print(len(rows)); 
for r in rows[-25:]: print(r)
```