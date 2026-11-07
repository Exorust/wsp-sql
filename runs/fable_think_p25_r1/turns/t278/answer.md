```python
# Hypothesis: native format ('<think>\n\n</think>') yields higher gold-SQL lp than ours; also check p(</think>) after '<think>\n\n' and neuron activations there.
F15=W+'/fwd_15'; tl15=np.load(F15+'/token_logprobs.npy'); tk15=np.load(F15+'/topk_ids.npy'); tkl15=np.load(F15+'/topk_logprobs.npy')
m15=json.load(open(F15+'/meta.json')); L15=m15['lengths']
texts15=OURS+NAT
res=[]
for k in range(12):
    ids_o=tok.encode(OURS[k]).ids; ids_n=tok.encode(NAT[k]).ids
    a=[i for i in range(len(ids_o)) if ids_o[i-1]==tok.encode('<think>').ids[-1]][0]  # index of token after <think>
    # ours: ids_o[a]='\n'(198), ids_o[a+1]=</think>; native: ids_n[a]='\n\n'(271), ids_n[a+1]=</think>
    assert ids_o[a]==198 and ids_n[a]==271 and ids_o[a+1]==END[0] and ids_n[a+1]==END[0]
    sql_o=float(np.nanmean(tl15[k,a+3:L15[k]])); sql_n=float(np.nanmean(tl15[12+k,a+3:L15[12+k]]))
    res.append((round(float(tl15[k,a]),2), round(float(tl15[12+k,a]),2), round(float(tl15[k,a+1]),2), round(float(tl15[12+k,a+1]),2), round(sql_o,3), round(sql_n,3)))
print('cols: lp(\\n|ours) lp(\\n\\n|nat) lp(</think>|ours) lp(</think>|nat) sqlmean_ours sqlmean_nat')
for r_ in res: print(r_)
print('mean sql lp ours %.3f nat %.3f'%(np.mean([r_[4] for r_ in res]),np.mean([r_[5] for r_ in res])))
```