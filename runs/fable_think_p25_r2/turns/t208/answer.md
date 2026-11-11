```python
# Collect model predictions at decision points (after SELECT, after FROM-table[alias], end of query)
inv={v[0]:k for k,v in kw.items() if len(v)==1}
def topk_lp(i,q,tid):
    row=tk12[i,q-1]; m=np.where(row==tid)[0]
    return float(tkl12[i,q-1,m[0]]) if len(m) else None
dec=[]
for i,ids in enumerate(T12):
    s=starts[i]; sql=ids[s:]
    end_q=s+len(sql)-1-2  # position of '\n' before closing fence: ids[-3]=='\n'? check
    assert ids[end_q]==198 and tok.decode([ids[end_q+1]]).startswith('`'), (tok.decode(ids[end_q:]),)
    # after SELECT
    qs=s+1
    # FROM-table decision
    fpos=[q for q in range(s,end_q) if ids[q]==enc(' FROM')[0]][0]
    q=fpos+2
    while q<end_q and ids[q] not in (12693,5120,26008,15064,198,5574,10067,28382,74902,3927,462): q+=1
    if ids[q]==5574: q+=2
    dec.append(dict(i=i,kind=kind(setC[i]['gold']),
        distinct_lp=topk_lp(i,qs,57088), gold_after_select=tok.decode([ids[qs]]), gold_after_select_lp=float(lp12[i,qs]),
        from_gold=tok.decode([ids[q]]), from_gold_lp=float(lp12[i,q]), from_top=tok.decode([tk12[i,q-1,0]]), from_top_lp=float(tkl12[i,q-1,0]),
        from_join_lp=topk_lp(i,q,12693), from_where_lp=topk_lp(i,q,5120), from_nl_lp=topk_lp(i,q,198),
        end_lp=float(lp12[i,end_q]), end_top=tok.decode([tk12[i,end_q-1,0]]), end_top_lp=float(tkl12[i,end_q-1,0]), end_2nd=tok.decode([tk12[i,end_q-1,1]]), end_2nd_lp=float(tkl12[i,end_q-1,1]),
        q_from=q, q_end=end_q, q_sel=qs))
dd=pd.DataFrame(dec)
pd.set_option('display.width',250); pd.set_option('display.max_columns',30)
print(dd[['i','kind','distinct_lp','gold_after_select','gold_after_select_lp','from_gold','from_gold_lp','from_top','from_top_lp','from_join_lp','from_where_lp','from_nl_lp']].round(2).to_string())
```