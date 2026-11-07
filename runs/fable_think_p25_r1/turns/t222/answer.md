```python
# Assemble req13: 10 loop texts (gen capped at 160 tokens) + 20 correct multi-line texts; mlp_act L16-23, hidden L23,24
def cap_tokens(t, n):
    ids=tok.encode(t).ids
    return tok.decode(ids[:n]) if len(ids)>n else t
loop_ids=['sp6955','sp914','sp4875','sp3831','sp2598','sp7','sp5081','sp6953','sp5600','sp303']
texts13=[]; info13=[]
for pid in loop_ids:
    r=allr[pid]; t=cap_tokens(truncate_loop(r['text']),160)
    texts13.append("<|im_start|>user\n"+prompt_of(pid)+"<|im_end|>\n<|im_start|>assistant\n<think>\n"+t); info13.append({'id':pid,'kind':'loop'})
for r in corr[:20]:
    texts13.append(gen_text(r)+"<|im_end|>\n"); info13.append({'id':r['id'],'kind':'correct'})
req13={'type':'teacher_forced','model':'edited','texts':texts13,'return':{'token_logprobs':True,'topk':10,'mlp_act':[16,17,18,19,20,21,22,23],'hidden_states':[23,24]}}
s13=json.dumps(req13).replace(FENCE,'\\u0060\\u0060\\u0060')
json.dump(info13,open(f'{W}/req13_items.json','w')); open(f'{W}/req13.json','w').write(s13)
print(len(texts13), len(s13), sum(len(tok.encode(t).ids) for t in texts13))
print(repr(texts13[1][-400:]))
```