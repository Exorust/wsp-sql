```python
# For each '\n' position in the SQL region, record: next token (gold-forced), lp of next token, lp of fence(71093) and AND/OR/JOIN in topk, and whether previous line is a repeat
def topk_lp(k,p,tid):
    row=tk_ids[k,p]; 
    j=np.where(row==tid)[0]
    return float(tk_lp[k,p,j[0]]) if len(j) else None
recs=[]
for k,ids in enumerate(enc13):
    s=starts[k]; seen=set(); line_tokens=[]
    kind=info13[k]['kind']
    for p in range(s, len(ids)-1):
        if ids[p]==198:
            line=tok.decode(line_tokens).strip(); rep= line in seen; seen.add(line); line_tokens=[]
            nxt=ids[p+1]
            # logprobs at position p predict token p+1: token_logprobs[k,p+1] is lp of ids[p+1]; topk at p+1 likewise (check convention)
            recs.append(dict(k=k,kind=kind,p=p,rep=rep,line=line[:40],nxt=tok.decode([nxt]),lp_next=float(lp13[k,p+1]),
                             lp_fence=topk_lp(k,p+1,71093),lp_and=topk_lp(k,p+1,3843),lp_or=topk_lp(k,p+1,842),lp_join=topk_lp(k,p+1,72910),
                             top1=tok.decode([int(tk_ids[k,p+1,0])]), top1lp=float(tk_lp[k,p+1,0])))
        else: line_tokens.append(ids[p])
# sanity: check convention: lp13[k,p] should be lp of ids[p] given prefix; verify with the topk at the fence positions in correct texts
import pandas as pd
df=pd.DataFrame(recs); print(len(df))
print(df[df.kind=='correct'][['k','line','nxt','lp_next','lp_fence','lp_and','top1','top1lp']].to_string()[:3000])
```