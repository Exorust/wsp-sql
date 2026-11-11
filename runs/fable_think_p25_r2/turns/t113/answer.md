```python
# Proper DLA (final residual = H23 + attn23 + mlp23): per-layer-23 head contributions to logit(NLNL)-logit(NL) at bullet-line ends
ids6=[tok.encode(req['texts'][i]).ids for i in sel_idx]
dNL=((E[271]-E[198])*(1+wn)).numpy()
def decision_positions(idsn):
    out=[]
    for i in range(len(idsn)-1):
        if idsn[i+1] in (198,271):
            # find start of current line
            j=i
            while j>0 and idsn[j]!=198 and idsn[j]!=271: j-=1
            line=tok.decode(idsn[j+1:i+1])
            if line.strip().startswith('*'): out.append((i, idsn[i+1], line.strip()[:60]))
    return out
for n in range(2):
    T=lens6[n]; mlp=M23_6[n,:T].astype(np.float32)@Wd23.T; hf=H23_6[n,:T].astype(np.float32)+HO[n].sum(0)+mlp
    r=np.sqrt((hf**2).mean(1))
    tot=(hf@dNL)/r; res23=(H23_6[n,:T].astype(np.float32)@dNL)/r; mlpc=(mlp@dNL)/r
    heads=np.stack([(HO[n][h]@dNL)/r for h in range(8)])   # [8,T]
    print(f'== text {n}; loop start token {m5[sel_idx[n]]["start"]}')
    for (i,nxt,line) in decision_positions(ids6[n]):
        print(f'{i:4d} next={"NLNL" if nxt==271 else "NL  "} tot={tot[i]:6.2f} res<=22={res23[i]:6.2f} mlp23={mlpc[i]:5.2f} heads=' + ' '.join(f'{heads[h,i]:5.2f}' for h in range(8)) + ' |', line[:45])
```