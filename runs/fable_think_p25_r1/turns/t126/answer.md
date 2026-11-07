```python
# Load fwd_7 results; tokenise texts; locate key tokens (</think>, bullet markers) and check p(</think>) at line starts
F=W+'/fwd_7/'
lp=np.load(F+'token_logprobs.npy'); tk=np.load(F+'topk_ids.npy'); tlp=np.load(F+'topk_logprobs.npy')
print(lp.shape, tk.shape)
enc=[tok.encode(t).ids for t in texts]
TH=tok.encode('</think>').ids; print('</think> ids', TH, [tok.decode([i]) for i in TH])
for s in ['\n\n','\n','*','   ',' Wait',' The',' So','\n    ',' *',' Okay','</think>','\n</think>']:
    print(repr(s), tok.encode(s).ids)
# positions of </think> in texts 0,4,5 and the logprob assigned, with topk
th_id=TH[0]
for i in [0,4,5]:
    ids=enc[i]
    pos=[j for j,x in enumerate(ids) if x==th_id]
    for j in pos:
        print(i, j, 'prev toks', repr(tok.decode(ids[j-6:j])), 'lp(</think>)=%.2f'%lp[i,j], 'top:', [(tok.decode([a]),round(float(b),2)) for a,b in zip(tk[i,j,:5],tlp[i,j,:5])])
```