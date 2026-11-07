```python
# Smaller request (72 texts, <=3 per db) so it can be pasted in ~6 chunks; add mlp_act L20-23 and hidden L23,24 for DLA analysis
sel=[];per=Counter()
for L,pid in cand:
    db=prac[pid]['db']
    if per[db]>=3: continue
    per[db]+=1; sel.append(pid)
    if len(sel)>=72: break
texts=[render(p,prac[p]['gold']) for p in sel]
req={'type':'teacher_forced','model':'edited','texts':texts,'return':{'token_logprobs':True,'topk':10,'mlp_act':[20,21,22,23],'hidden_states':[23,24]}}
s=json.dumps(req).replace(FENCE,'\\u0060\\u0060\\u0060')
print(len(sel), len(per), len(s), sum(len(tok.encode(t).ids) for t in texts))
json.dump({'tf_ids':sel}, open(f'{W}/req12_items.json','w')); open(f'{W}/req12.json','w').write(s)
CH=9600; print('chunks', (len(s)+CH-1)//CH)
print(s[:CH])
```