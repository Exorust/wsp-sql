```python
# For each gold chat: find SQL region tokens, and at each position print gold token vs model top-1 where they disagree (structural tokens)
def analyze(i, show=True):
    ids=tok.encode(texts[i]).ids; L=len(ids)
    toks=[tok.decode([t]) for t in ids]
    # find start of ```sql in assistant
    s=texts[i].rfind('```sql\n'); 
    # locate token index where SQL starts: cumulative decode
    pos=0; start=None
    for j,t in enumerate(toks):
        pos+=len(t)
        if start is None and pos>s+7: start=j
    out=[]
    for j in range(start, L-1):
        gold=ids[j+1]; top=tk[i,j,0]
        if gold!=top:
            out.append((j, toks[j+1], tok.decode([int(top)]), float(lp[i,j+1]) if j+1<lp.shape[1] else None, float(tkl[i,j,0])))
    if show:
        print('---',meta_ids[i], 'nSQLtoks', L-start, 'mismatches', len(out))
        for o in out[:14]: print('   gold %r (lp %.2f)  vs top %r (%.2f)'%(o[1],o[3],o[2],o[4]))
    return out
meta_ids=json.load(open(os.path.join(W,'tf12_meta.json')))['ids']
# check alignment of lp: token_logprobs[i,t] is logprob of token t given previous
print('lp[0,1:6]',lp[0,1:6])
for i in range(4): analyze(i)
```