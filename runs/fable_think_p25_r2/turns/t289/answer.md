```python
# Dose-response alpha=6 vs 3 vs 0 on same gold chats
R['steer6']=analyze(W+'/fwd_15')
for k in ['plain','steer3','steer6']:
    o=R[k]; print(k, 'sql %.2f  sel_gold %.2f sel_dist %.2f from_gold %.2f think %.3f first_sql %.2f  DISTINCT-top1 %d  alias-top1 %d'%(np.mean(o['sql']),np.mean(o['sel_gold']),np.mean(o['sel_dist']),np.mean(o['from_gold']),np.mean(o['think']),np.mean(o['first_sql']),sum(t=='DISTINCT' for t in o['sel_top']),sum(len(t)<=2 and t.isalpha() for t in o['sel_top'])))
print('per-problem sql delta steer6-plain:', np.round(np.array(R['steer6']['sql'])-np.array(R['plain']['sql']),1))
print('from_top steer6:', R['steer6']['from_top']); print('sel_top steer6:', R['steer6']['sel_top'])
# also: total logprob over the whole assistant text incl. formatting (sanity), and worst token
lp6=np.load(W+'/fwd_15/token_logprobs.npy'); lp3=np.load(W+'/fwd_14/token_logprobs.npy')
print('min token lp over SQL spans: plain %.2f steer3 %.2f steer6 %.2f'%(np.mean([lp[j,my_sql_span(T[j])[0]:my_sql_span(T[j])[1]].min() for j in range(32)]),np.mean([lp3[j,my_sql_span(T[j])[0]:my_sql_span(T[j])[1]].min() for j in range(32)]),np.mean([lp6[j,my_sql_span(T[j])[0]:my_sql_span(T[j])[1]].min() for j in range(32)])))
```