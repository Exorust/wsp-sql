```python
# How general is the line-end decision? Check loop periods for NL token and bullet pattern; collect per-text loop info
loopinfo={}
cnt_nl=0; cnt_bullet=0
for i,(gid,o,p,n) in enumerate(onsets):
    if o is None: continue
    ids=tok.encode(gens[i]['text']).ids
    per=ids[o:o+p]
    has_nl = NL in per
    has_bullet = (348 in per)  # ' *'
    cnt_nl+=has_nl; cnt_bullet+=has_bullet
    loopinfo[gid]=(o,p,has_nl,has_bullet)
print("loops with NL in period:",cnt_nl,"with bullet:",cnt_bullet,"of",len(loopinfo))
# examples without NL
for gid,(o,p,hn,hb) in loopinfo.items():
    if not hn:
        ids=tok.encode(gen_by_id[gid]['text']).ids
        print(gid, p, repr(tok.decode(ids[o:o+p]))[:120])
```