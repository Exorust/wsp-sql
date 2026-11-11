```python
# Compare fwd_9 (orig) and fwd_10 (edited) logprobs at the '</think>' position of T2 texts (eval template, immediate end)
ids_think_end=tok.encode('</think>').ids; print('</think> ids',ids_think_end, 'think ids',tok.encode('<think>').ids, 'NL',tok.encode('\n').ids, tok.encode('\n\n').ids)
def enc(t): return tok.encode(t).ids
lp9=np.load(f'{W}/fwd_9/token_logprobs.npy'); lp10=np.load(f'{W}/fwd_10/token_logprobs.npy')
tk9=np.load(f'{W}/fwd_9/topk_ids.npy'); tkl9=np.load(f'{W}/fwd_9/topk_logprobs.npy')
tk10=np.load(f'{W}/fwd_10/topk_ids.npy'); tkl10=np.load(f'{W}/fwd_10/topk_logprobs.npy')
texts9=r9['texts']; texts10=r10['texts']
def positions(text):
    ids=enc(text); 
    # find </think> token
    te=ids_think_end[0]
    pos=[i for i,t in enumerate(ids) if t==te]
    return ids,pos
for i,t in enumerate(texts10):
    ids,pos=positions(t); p=pos[0]
    j9=[k for k,(kind,pid) in enumerate(r9_meta['kinds']) if kind=='T2' and pid==json.load(open(f'{W}/tf10_meta.json'))['kinds'][i][1]] if (r9_meta:=json.load(open(f'{W}/tf9_meta.json'))) else []
    s='orig lp(</think>)=%s'%(lp9[j9[0],p] if j9 else 'NA')
    # SQL tokens after </think>: mean logprob
    sql_lp10=lp10[i,p+1:len(ids)].mean(); sql_lp9=lp9[j9[0],p+1:len(ids)].mean() if j9 else np.nan
    print(i, 'pos',p,'edited lp(</think>)=%.2f'%lp10[i,p], s, '| mean lp after: ed %.3f orig %.3f'%(sql_lp10,sql_lp9))
    print('   edited top5 ids', tk10[i,p,:5].tolist(), np.round(tkl10[i,p,:5],2).tolist())
```