```python
# Hypothesis: at gold decision points the model puts high prob on over-complication tokens (DISTINCT after SELECT, alias/JOIN after FROM table)
tk_ids=np.load(d+'topk_ids.npy'); tk_lp=np.load(d+'topk_logprobs.npy')
def tid(s): return tok.encode(s,add_special_tokens=False).ids
print('DISTINCT ids', tid(' DISTINCT'), tid(' distinct'), 'JOIN', tid(' JOIN'), tid(' AS'), 'WHERE', tid(' WHERE'), 'T1',tid(' T'))
stats=[]
for j in range(32):
    enc=tok.encode(T[j]); ids=enc.ids; offs=enc.offsets
    a0,b0,_=my_sql_span(T[j])
    toks=[T[j][x:y] for x,y in offs]
    # position where gold token 'SELECT' sits -> prediction at next position is lp[j, p+1]? token_logprobs[i] = logprob of token i given prefix. topk at index i is distribution for token i.
    for p in range(a0,b0):
        if toks[p].strip().upper()=='SELECT' and p+1<b0:
            q=p+1; nxt=toks[q]
            row=dict(zip(tk_ids[j,q].tolist(),tk_lp[j,q].tolist()))
            pd=max([row.get(t,-99) for t in tid(' DISTINCT')+tid(' distinct')])
            stats.append(('SEL',j,nxt,pd,lp[j,q]))
    # after FROM <table>: find token 'FROM', then table tokens until space-keyword
    for p in range(a0,b0):
        if toks[p].strip().upper()=='FROM':
            q=p+1
            while q<b0 and not toks[q].startswith(' '): q+=1
            q+=1
            while q<b0 and not toks[q].startswith(' '): q+=1
            if q<b0:
                row=dict(zip(tk_ids[j,q].tolist(),tk_lp[j,q].tolist()))
                pj=max([row.get(t,-99) for t in tid(' JOIN')]); pa=max([row.get(t,-99) for t in tid(' AS')])
                stats.append(('FROM',j,toks[q],pj,pa,lp[j,q]))
            break
for s in stats[:40]: print(s)
```