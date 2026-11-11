```python
# Paired comparison gen_16 (skip-think + steer6) vs gen_11 (skip-think only) on same 128 ids
G16={g['id']:g for g in (json.loads(l) for l in open(W+'/gen_16.jsonl'))}; G11={g['id']:g for g in G}
c11=np.array([G11[i]['cls']=='correct' for i in ids11]); c16=np.array([G16[i]['cls']=='correct' for i in ids11])
dlt=c16.astype(int)-c11.astype(int); print('acc 11: %.3f  16: %.3f  diff %.3f +- %.3f  w->r %d  r->w %d'%(c11.mean(),c16.mean(),dlt.mean(),dlt.std(ddof=1)/np.sqrt(len(dlt)),(dlt==1).sum(),(dlt==-1).sum()))
# structural stats of edited answers vs gold
for nm,GG in [('gen11',G11),('gen16',G16)]:
    cnt=Counter()
    for i in ids11:
        a=feats(GG[i]['sql'] or ''); b=feats(P[i]['gold'])
        cnt['join_extra']+=a['join'] and not b['join']; cnt['join_missing']+=b['join'] and not a['join']; cnt['distinct_extra']+=a['distinct'] and not b['distinct']; cnt['has_join']+=a['join']; cnt['has_distinct']+=a['distinct']
    print(nm, dict(cnt))
import shutil; os.makedirs(W+'/best_2',exist_ok=True)
for f in os.listdir(W+'/edited'): shutil.copy(W+'/edited/'+f, W+'/best_2/'+f)
print(os.listdir(W+'/best_2'))
```