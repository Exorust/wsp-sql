```python
# fwd_13: does the simplicity instruction raise gold-SQL logprob? Per-problem paired diff over SQL tokens; and at the SELECT+1 position
F13=os.path.join(W,'fwd_13'); lp13=np.load(os.path.join(F13,'token_logprobs.npy')); tk13=np.load(os.path.join(F13,'topk_ids.npy')); tkl13=np.load(os.path.join(F13,'topk_logprobs.npy'))
T13=texts13; N=32
ST13=[sql_start(t) for t in T13]; LEN13=[len(tok.encode(t).ids) for t in T13]
tot0=[];tot1=[];sel0=[];sel1=[];first0=[];first1=[]
for i in range(N):
    a,b=i,i+N
    s0=lp13[a,ST13[a]+1:LEN13[a]-1]; s1=lp13[b,ST13[b]+1:LEN13[b]-1]   # SQL tokens incl. '\n' and fence? up to <|im_end|>
    assert len(s0)==len(s1)
    tot0.append(s0.sum()); tot1.append(s1.sum())
    first0.append(lp13[a,ST13[a]+1]); first1.append(lp13[b,ST13[b]+1])   # token after SELECT
d=np.array(tot1)-np.array(tot0)
print('sum logprob of gold SQL per problem: V0 mean %.2f, V1 mean %.2f, paired diff mean %.2f +- %.2f'%(np.mean(tot0),np.mean(tot1),d.mean(),d.std()/np.sqrt(N)))
print('n improved', (d>0).sum(), 'of', N)
df1=np.array(first1)-np.array(first0)
print('logprob of gold token right after SELECT: V0 %.2f V1 %.2f, diff %.2f +- %.2f'%(np.mean(first0),np.mean(first1),df1.mean(),df1.std()/np.sqrt(N)))
for i in range(N):
    a,b=i,i+N; j=ST13[a]
    print(pool[i], 'gold', S(repr(tok.decode([tok.encode(T13[a]).ids[j+1]]))), 'V0 %.2f V1 %.2f'%(first0[i],first1[i]), '| V0 top', topk_at.__wrapped__(a,j,3) if hasattr(topk_at,'__wrapped__') else [(S(tok.decode([int(t)])),round(float(l),2)) for t,l in zip(tk13[a,j,:3],tkl13[a,j,:3])], '| V1 top', [(S(tok.decode([int(t)])),round(float(l),2)) for t,l in zip(tk13[b,j+0,:3],tkl13[b,j,:3])])
```