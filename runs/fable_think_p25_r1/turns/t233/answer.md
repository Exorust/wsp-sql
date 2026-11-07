```python
# Fix topk convention: topk[k,p] predicts ids[p+1]
recs=[]
for k,ids in enumerate(enc13):
    s=starts[k]; seen=set(); line_tokens=[]; kind=info13[k]['kind']
    for p in range(s, len(ids)-1):
        if ids[p]==198:
            line=tok.decode(line_tokens).strip(); rep= line in seen; seen.add(line); line_tokens=[]
            nxt=ids[p+1]
            recs.append(dict(k=k,kind=kind,p=p,rep=rep,line=line[:40],nxt=tok.decode([nxt]),lp_next=float(lp13[k,p+1]),
                             lp_fence=topk_lp(k,p,71093),lp_and=topk_lp(k,p,3843),lp_or=topk_lp(k,p,842),lp_join=topk_lp(k,p,72910),
                             top1=tok.decode([int(tk_ids[k,p,0])]), top1lp=float(tk_lp[k,p,0]), top2=tok.decode([int(tk_ids[k,p,1])]), top2lp=float(tk_lp[k,p,1])))
        else: line_tokens.append(ids[p])
df=pd.DataFrame(recs)
pd.set_option('display.width',250)
print(df[df.kind=='correct'][['k','line','nxt','lp_next','lp_fence','top1','top1lp','top2','top2lp']].to_string()[:4000])
```