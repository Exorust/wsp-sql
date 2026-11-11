```python
# Per-layer DLA of logit(</think>) - logit('Thinking') at the token after <think> for T1 ('\n\n') vs T2 ('\n')
H9=[np.load(os.path.join(d9,f'hidden_L{l}.npy'), mmap_mode='r') for l in range(25)]
def dla_at(i,pos,a,b): return layer_dla(H9,i,pos,a,b)
res={}
for i,(kind,pid) in enumerate(kinds9[:8]):
    pos=ids9[i].index(248068)+1
    c,tot=dla_at(i,pos,TH,THINKING); res.setdefault(kind,[]).append(c)
for kind in ['T1','T2']:
    c=np.stack(res[kind]).mean(0); print(kind, 'total %.1f'%c.sum()); print(np.round(c,2))
print('diff T1-T2 per layer:'); print(np.round(np.stack(res['T1']).mean(0)-np.stack(res['T2']).mean(0),2))
```