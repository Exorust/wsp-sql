```python
# Hypothesis: the 4 start-of-thinking neurons are quiet outside the trigger position in edited-model texts (fwd_13), so raising alpha is safe; also check whether </think> ever enters top-10 elsewhere.
neur={17:537,18:628,19:2424,20:1235}
END=tok.encode('</think>').ids; print('</think> ids',END)
lens=meta['lengths']
for L,n in neur.items():
    A=np.load(F+'/mlp_down_in_L%d.npy'%L)[:,:,n].astype(np.float32)
    trig=[];rest=[]
    for k in range(21):
        ids=ids13[k]; pos=[i for i in range(1,lens[k]) if ids[i-1]==END[0] or tok.decode(ids[i-1:i+1]).endswith('<think>\n')]
        # trigger position = index of the '\n' right after '<think>'
        tpos=[i for i in range(lens[k]) if tok.decode(ids[max(0,i-1):i+1])=='<think>\n']
        for i in range(lens[k]):
            (trig if i in tpos else rest).append(A[k,i])
    rest=np.array(rest); print('L%d n%d trigger acts'%(L,n),np.round(trig[:4],2),'| rest max',round(float(rest.max()),2),'p99.9',round(float(np.quantile(rest,0.999)),2),'min',round(float(rest.min()),2))
# </think> in top10 elsewhere?
cnt=0
for k in range(21):
    for i in range(lens[k]):
        if END[0] in tk[k,i] and tok.decode(ids13[k][max(0,i-1):i+1])!='<think>\n': cnt+=1
print('positions with </think> in top10 outside trigger:',cnt)
```