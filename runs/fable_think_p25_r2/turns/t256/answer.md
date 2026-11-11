```python
# Hypothesis: INSTR1 in the prompt raises gold-SQL logprob (measures how much a 'be simple/exact' direction could help)
d=W+'/fwd_13/'; lp=np.load(d+'token_logprobs.npy'); meta=json.load(open(d+'meta.json'))
L=[int(x) for x in meta['lengths'].strip('[],').split(',') if x.strip()]
def sql_span(text):
    # token index range of assistant SQL (after '```sql\n' up to '```')
    ids=tok.encode(text).ids
    s=text.index('```sql\n',text.index('<|im_start|>assistant'))+len('```sql\n'); e=text.index('```',s)
    # map char->token via decode prefix lengths
    pos=0; starts=[]
    for i,t in enumerate(ids):
        starts.append(len(tok.decode(ids[:i+1])))
    i0=next(i for i,c in enumerate(starts) if c>s); i1=next(i for i,c in enumerate(starts) if c>=e)
    return i0,i1,len(ids)
res=[]
for j in range(32):
    a0,b0,n0=sql_span(T[j]); a1,b1,n1=sql_span(T[32+j])
    assert n0==L[j] and n1==L[32+j], (n0,L[j],n1,L[32+j])
    s0=lp[j,a0:b0]; s1=lp[32+j,a1:b1]
    res.append((s0.sum(),s1.sum(),b0-a0,s0.min(),s1.min()))
res=np.array(res); print('mean gold-SQL sum logprob plain %.2f  I1 %.2f ; per-token %.3f vs %.3f'%(res[:,0].mean(),res[:,1].mean(),(res[:,0]/res[:,2]).mean(),(res[:,1]/res[:,2]).mean()))
print('n improved', (res[:,1]>res[:,0]).sum(), 'of 32; min-token plain %.2f I1 %.2f'%(res[:,3].mean(),res[:,4].mean()))
```