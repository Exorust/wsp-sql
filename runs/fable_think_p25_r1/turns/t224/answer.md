```python
# Slimmer req13: 7 loop texts + 14 correct multi-line texts
loop_ids=['sp6955','sp914','sp4875','sp3831','sp2598','sp6953','sp5600']
texts13=[]; info13=[]
for pid in loop_ids:
    r=allr[pid]; t=cap_tokens(truncate_loop(r['text']),160)
    texts13.append("<|im_start|>user\n"+prompt_of(pid)+"<|im_end|>\n<|im_start|>assistant\n<think>\n"+t); info13.append({'id':pid,'kind':'loop'})
for r in corr[:14]:
    texts13.append(gen_text(r)+"<|im_end|>\n"); info13.append({'id':r['id'],'kind':'correct'})
req13={'type':'teacher_forced','model':'edited','texts':texts13,'return':{'token_logprobs':True,'topk':10,'mlp_act':[16,17,18,19,20,21,22,23],'hidden_states':[23,24]}}
s13=json.dumps(req13).replace(FENCE,'\\u0060\\u0060\\u0060')
json.dump(info13,open(f'{W}/req13_items.json','w')); open(f'{W}/req13.json','w').write(s13)
CH=9800; nch=(len(s13)+CH-1)//CH
print(len(texts13), len(s13), nch, sum(len(tok.encode(t).ids) for t in texts13))
print(s13[0:CH])
```