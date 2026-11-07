```python
# Hypothesis: in answer loops, the decision points are at clause boundaries ('\n' -> 'AND' vs '```'/'ORDER'); find low-margin positions in the loop region of texts 3-6.
for k,astart,p,onset in loop_info[3:]:
    ids=ids13[k]; n=len(ids)
    print('== text',k,it13[k]['id'],'period',p)
    for i in range(onset+p, n):  # position i predicted from i-1; token_logprobs[k,i] is lp of ids[i]
        lp=tl[k,i]; alt=[(tok.decode([int(t)]),round(float(l),2)) for t,l in zip(tk[k,i],tkl[k,i]) if int(t)!=ids[i]][:3]
        margin=lp-alt[0][1]
        if margin<2.5: print('  pos',i,'tok',repr(tok.decode(ids[i-2:i+1]))[-40:],'lp',round(float(lp),2),'alts',alt)
```