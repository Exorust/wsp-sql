```python
# Hypothesis: at the hallucination decision token, a valid column token is close behind; per-neuron DLA (L16-23) reveals consistent 'wrong>valid' pushers
D=f'{W}/fwd_17'; lp17=np.load(f'{D}/token_logprobs.npy'); tk17=np.load(f'{D}/topk_ids.npy'); tkl17=np.load(f'{D}/topk_logprobs.npy')
H24=np.load(f'{D}/hidden_L24.npy')
def parse_cols(db):
    cols={}
    for blk in schema(db).split('CREATE TABLE')[1:]:
        head,body=blk.split('(',1); tname=head.strip().strip('"`[]').lower()
        body=body.rsplit(')',1)[0]
        cl=[]
        depth=0; cur=''
        for ch in body:
            if ch=='(': depth+=1
            if ch==')': depth-=1
            if ch==',' and depth==0: cl.append(cur); cur=''
            else: cur+=ch
        cl.append(cur)
        names=[]
        for it in cl:
            w=it.strip().split()
            if not w: continue
            if w[0].upper() in ('PRIMARY','FOREIGN','CONSTRAINT','UNIQUE','CHECK','KEY'): continue
            names.append(w[0].strip('"`[]'))
        cols[tname]=names
    return cols
def strip_tok(s): return s.lstrip(' .("`[')
dec=[]
for i,c in enumerate(short_err):
    cols=parse_cols(c['db']); sql=c['text'][c['text'].rfind(F+'sql'):]
    amap={}
    for m in re.finditer(r'(?:FROM|JOIN)\s+["`]?(\w+)["`]?\s+(?:AS\s+)?(?!ON|WHERE|JOIN|GROUP|ORDER|LEFT|INNER)(\w+)', sql, re.I): amap[m.group(2).lower()]=m.group(1).lower()
    tables=[m.group(1).lower() for m in re.finditer(r'(?:FROM|JOIN)\s+["`]?(\w+)',sql,re.I)]
    if '.' in c['col']:
        al=c['col'].split('.')[0].lower(); t=amap.get(al, al); valid=[x for x in cols.get(t,[])]
    else:
        valid=[x for t in tables for x in cols.get(t,[])]
    validl=[v.lower() for v in valid]
    enc=tok.encode(c['text']); ids=enc.ids
    acc=''; d=None
    for p in range(c['pos'], len(ids)):
        s=tok.decode([ids[p]]); stem=strip_tok(s) if p==c['pos'] else s
        if any(v.startswith((acc+stem).lower()) for v in validl): acc+=stem; continue
        d=p; break
    if d is None: continue
    # valid alternatives in topk at d
    alts=[]
    for t,l in zip(tk17[i,d],tkl17[i,d]):
        s=tok.decode([int(t)]); stem=strip_tok(s) if d==c['pos'] else s
        if stem and any(v.startswith((acc+stem).lower()) and len(acc+stem)>len(acc) for v in validl): alts.append((s,float(l)))
    chosen=tok.decode([ids[d]]); dec.append({'i':i,'d':d,'chosen':chosen,'lp':float(lp17[i,d]),'alts':alts[:3],'valid':valid[:6],'acc':acc})
    print(c['id'], c['col'], '| d',d,'chosen',repr(chosen), round(float(lp17[i,d]),2), '| best valid', alts[:2], '| table cols', valid[:5])
print(len(dec))
```