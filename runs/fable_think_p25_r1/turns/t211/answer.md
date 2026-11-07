```python
# Pick a compact set: ~110 fresh problems with the shortest prompts (distinct dbs varied) to keep the inline request ~150KB
cand=[]
for pid in pool[1000:]:
    t=render(pid, prac[pid]['gold']); cand.append((len(t),pid))
cand.sort()
# diversify dbs: at most 4 per db
sel=[];per=Counter()
for L,pid in cand:
    db=prac[pid]['db']
    if per[db]>=4: continue
    per[db]+=1; sel.append(pid)
    if len(sel)>=110: break
texts=[render(p,prac[p]['gold']) for p in sel]
s=json.dumps({'type':'teacher_forced','model':'edited','texts':texts,'return':{'token_logprobs':True,'topk':10}}).replace(FENCE,'\\u0060\\u0060\\u0060')
print(len(sel), len(per), len(s), sum(len(tok.encode(t).ids) for t in texts))
json.dump({'tf_ids':sel}, open(f'{W}/req12_items.json','w')); open(f'{W}/req12.json','w').write(s)
print(s[:300])
```