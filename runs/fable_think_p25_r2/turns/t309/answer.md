```python
# Record dose-response; restore x1.0 steering; inspect wrong_result examples in gen_16 (pred vs gold) for dominant patterns
rows18=[json.loads(l) for l in open(os.path.join(W,'gen_18.jsonl'))]; r18={r['id']:r for r in rows18}
cm=[i for i in r18 if i in r16]; a16=np.array([r16[i]['cls']=='correct' for i in cm]); a18=np.array([r18[i]['cls']=='correct' for i in cm]); d=a16.astype(float)-a18
print('x1.0 vs x1.6 paired n',len(cm),'acc',a16.mean().round(3),a18.mean().round(3),'diff',d.mean().round(3),'se',(d.std()/np.sqrt(len(d))).round(3))
Wd=load_original('model.language_model.layers.16.mlp.down_proj.weight').clone(); Wd[:,3]=torch.tensor(c3); save_edit('model.language_model.layers.16.mlp.down_proj.weight', Wd)
with open(os.path.join(W,'notes.md'),'a') as f:
    f.write("- gen_17 (L18 only, gen_16 ids, 116 overlap): acc 30.2% vs 36.2% with L16 => L16 steer +6.0 (se 3.7), 13 w->r, 6 r->w. gen_18 (L16 x1.6): 28.1% => overshoot hurts; x1.0 (15.6*v16) kept. best_1 = current.\n")
gold={}
for l in open('/Users/chandu/myproj/wsp-sql/practice/spider_train.jsonl'):
    o=json.loads(l); gold[o['id']]=o
wr=[r for r in rows if r['cls']=='wrong_result']
for r in wr[:14]:
    print('--',r['id'],'| Q:',gold[r['id']]['question'][:90]); print('   P:',r['sql'][:150].replace('\n',' ')); print('   G:',gold[r['id']]['gold'][:150])
```