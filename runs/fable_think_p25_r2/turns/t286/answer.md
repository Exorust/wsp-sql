```python
# Compare steer (alpha=3) vs plain vs INSTR1: gold-SQL logprob, decision points, DISTINCT top1 count, and </think> at '<think>\n'
def analyze(dirn, offset=0, n=32):
    lpx=np.load(dirn+'/token_logprobs.npy'); ti=np.load(dirn+'/topk_ids.npy'); tl=np.load(dirn+'/topk_logprobs.npy')
    out=dict(sql=[],sel_gold=[],sel_dist=[],from_gold=[],sel_top=[],from_top=[],think=[],first_sql=[])
    for j in range(n):
        jj=j+offset
        a0,b0,_=my_sql_span(T[j]); out['sql'].append(float(lpx[jj,a0:b0].sum()))
        enc=tok.encode(T[j]); toks=[T[j][x:y] for x,y in enc.offsets]
        # </think> position: token index of '</think>' in assistant part
        pth=[i for i,t in enumerate(toks) if t=='</think>'][0]; out['think'].append(float(lpx[jj,pth]))
        out['first_sql'].append(float(lpx[jj,a0]))
        dp,_=decision_points(j)
        p=dp['SEL']; row=dict(zip(ti[jj,p].tolist(),tl[jj,p].tolist()))
        out['sel_gold'].append(float(lpx[jj,p+1])); out['sel_dist'].append(row.get(57088,-15)); out['sel_top'].append(tok.decode([int(ti[jj,p][0])]).strip())
        if 'FROM' in dp:
            q=dp['FROM']; out['from_gold'].append(float(lpx[jj,q+1])); out['from_top'].append(tok.decode([int(ti[jj,q][0])]).strip())
    return out
R={'plain':analyze(W+'/fwd_13'),'instr1':analyze(W+'/fwd_13',offset=32),'steer3':analyze(W+'/fwd_14')}
for k,o in R.items():
    print(k, 'sql %.2f  sel_gold %.2f sel_dist %.2f from_gold %.2f think %.3f first_sql %.2f  DISTINCT-top1 %d  alias-top1 %d'%(np.mean(o['sql']),np.mean(o['sel_gold']),np.mean(o['sel_dist']),np.mean(o['from_gold']),np.mean(o['think']),np.mean(o['first_sql']),sum(t=='DISTINCT' for t in o['sel_top']),sum(len(t)<=2 and t.isalpha() for t in o['sel_top'])))
print('per-problem sql delta steer3-plain:', np.round(np.array(R['steer3']['sql'])-np.array(R['plain']['sql']),1))
print('from_top plain :', R['plain']['from_top']); print('from_top steer3:', R['steer3']['from_top']); print('sel_top steer3:', R['steer3']['sel_top'])
```