```python
# Hypothesis: in the loop region, some heads attend to position t-P+1 (induction) or t-P (duplicate); compute per-head scores
F=W+'/fwd_2'
lp=np.load(F+'/token_logprobs.npy'); print(lp.shape)
ids0=tok.encode(texts2[0]).ids; ids1=tok.encode(texts2[1]).ids
L=[3,7,11,15,19,23]
def period_scores(ti, ids, P, loop_from):
    T=len(ids); res={}
    for l in L:
        A=np.load(F+f'/attn_L{l}_text{ti}.npy')  # heads,T,T
        H=A.shape[0]
        qs=np.arange(loop_from+P, T)
        ind=np.array([A[:,t,t-P+1] for t in qs]).mean(0)   # induction target
        dup=np.array([A[:,t,t-P] for t in qs]).mean(0)     # duplicate token
        ind2=np.array([A[:,t,t-2*P+1] for t in qs if t-2*P+1>=0]).mean(0)
        prev=np.array([A[:,t,t-1] for t in qs]).mean(0)
        self_=np.array([A[:,t,t] for t in qs]).mean(0)
        first=np.array([A[:,t,0] for t in qs]).mean(0)
        res[l]=dict(ind=ind,dup=dup,ind2=ind2,prev=prev,self=self_,first=first)
    return res
# text0: loop start at answer tok 449 -> abs 604, P=89; text1: abs 1016, P=35
S0=period_scores(0, ids0, 89, 604)
S1=period_scores(1, ids1, 35, 1016)
np.set_printoptions(precision=2, suppress=True, linewidth=150)
for l in L:
    print('L',l,'ind0',S0[l]['ind'],'\n     ind1',S1[l]['ind'])
    print('     dup0',S0[l]['dup'],'\n     dup1',S1[l]['dup'])
    print('     first0',S0[l]['first'],' self0',S0[l]['self'])
```