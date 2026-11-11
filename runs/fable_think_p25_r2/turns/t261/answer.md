```python
# Hypothesis: INSTR1 raises gold-SQL logprob; compute per problem with offsets
def my_sql_span(text):
    enc=tok.encode(text); offs=enc.offsets
    s=text.index(BT+'sql\n',text.index('<|im_start|>assistant'))+7; e=text.index(BT,s)
    i0=next(i for i,(a,b) in enumerate(offs) if b>s); i1=next(i for i,(a,b) in enumerate(offs) if a>=e)
    return i0,i1,len(enc.ids)
res=[]
for j in range(32):
    a0,b0,n0=my_sql_span(T[j]); a1,b1,n1=my_sql_span(T[32+j])
    s0=lp[j,a0:b0]; s1=lp[32+j,a1:b1]
    res.append((s0.sum(),s1.sum(),b0-a0,s0.min(),s1.min()))
res=np.array(res); print('mean gold-SQL sum logprob plain %.2f  I1 %.2f ; per-token %.3f vs %.3f'%(res[:,0].mean(),res[:,1].mean(),(res[:,0]/res[:,2]).mean(),(res[:,1]/res[:,2]).mean()))
print('n improved', (res[:,1]>res[:,0]).sum(), 'of 32; min-token plain %.2f I1 %.2f'%(res[:,3].mean(),res[:,4].mean()))
print(np.round(res[:,1]-res[:,0],1))
```