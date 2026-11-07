```python
# Compare pass 8 (edited v1) vs pass 4 (original) on the same 20 texts: decision margins in loop texts, SQL logprobs in gold texts
F4=W+'/fwd_4/'; F8=W+'/fwd_8/'
lp4=np.load(F4+'token_logprobs.npy'); tk4=np.load(F4+'topk_ids.npy'); tlp4=np.load(F4+'topk_logprobs.npy')
lp8=np.load(F8+'token_logprobs.npy'); tk8=np.load(F8+'topk_ids.npy'); tlp8=np.load(F8+'topk_logprobs.npy')
texts8=[r4['texts'][k] for k in sel]; enc8=[tok.encode(t).ids for t in texts8]
def lpof(tkrow,lprow,tid):
    w=np.where(tkrow==tid)[0]; return float(lprow[w[0]]) if len(w) else -25.
def bullet_end_margins(tkA,tlpA,a,ids):
    # a = row in array; positions j where ids[j] in (nl,nlnl) after sentence end; margin lp(nl)-lp(nlnl) predicted at j-1
    out=[]
    st=ids.index(tok.encode('<think>').ids[0])
    for j in range(st+1,len(ids)):
        if ids[j] in (198,271) and tok.decode([ids[j-1]]).strip().endswith(('.','`','?','!',')')):
            out.append((j, lpof(tkA[a,j-1],tlpA[a,j-1],198)-lpof(tkA[a,j-1],tlpA[a,j-1],271)))
    return out
def nlnl_margins(tkA,tlpA,a,ids):
    out=[]
    st=ids.index(tok.encode('<think>').ids[0])
    for j in range(st+1,len(ids)-1):
        if ids[j]==271:
            row=tkA[a,j]; lps=tlpA[a,j]
            bd=max([lpof(row,lps,d) for d in dig]); out.append((j, lpof(row,lps,id_ind)-bd))
    return out
for a in range(8):
    o=sel[a]; ids=enc8[a]
    be4=bullet_end_margins(tk4,tlp4,o,ids); be8=bullet_end_margins(tk8,tlp8,a,ids)
    nn4=nlnl_margins(tk4,tlp4,o,ids); nn8=nlnl_margins(tk8,tlp8,a,ids)
    m4=np.array([m for _,m in be4]); m8=np.array([m for _,m in be8])
    print(f'loop text {a}: bullet-ends n={len(m4)} orig median {np.median(m4):.2f} min {m4.min():.2f} #<0 {(m4<0).sum()} | edited median {np.median(m8):.2f} min {m8.min():.2f} #<0 {(m8<0).sum()}')
    print(f'   nlnl pts (ind - best digit): orig {[round(m,1) for _,m in nn4]} | edited {[round(m,1) for _,m in nn8]}')
```