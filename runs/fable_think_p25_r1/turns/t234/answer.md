```python
# Loop texts: at each line end (the position of the last token before '\n'), compare lp('\n') vs lp(';') and at the line start lp(AND/OR/JOIN) vs fence
SEMI=tok.encode('x;').ids[1]; print('semi id',SEMI, repr(tok.decode([SEMI])))
def topk_lp(k,p,tid):
    row=tk_ids[k,p]; j=np.where(row==tid)[0]
    return float(tk_lp[k,p,j[0]]) if len(j) else None
rows_=[]
for k,ids in enumerate(enc13):
    if info13[k]['kind']!='loop': continue
    s=starts[k]; seen=set(); line_tokens=[]
    for p in range(s, len(ids)):
        if ids[p]==198:
            line=tok.decode(line_tokens).strip(); rep=line in seen; seen.add(line); line_tokens=[]
            # at position p-1 the model predicted ids[p]='\n'
            rows_.append(dict(k=k,line=line[-38:],rep=rep,lp_nl=float(lp13[k,p]),lp_semi=topk_lp(k,p-1,SEMI),nl_top1=tok.decode([int(tk_ids[k,p-1,0])]),
                              nxt=tok.decode([ids[p+1]]) if p+1<len(ids) else None, lp_nxt=float(lp13[k,p+1]) if p+1<len(ids) else None,
                              lp_fence=topk_lp(k,p,71093), st_top2=tok.decode([int(tk_ids[k,p,1])]), st_top2lp=float(tk_lp[k,p,1])))
        else: line_tokens.append(ids[p])
dl=pd.DataFrame(rows_)
print(dl.to_string()[:9000])
```