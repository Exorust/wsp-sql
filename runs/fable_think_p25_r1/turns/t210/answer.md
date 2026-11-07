```python
# Verify render matches the format used in pass 10, then pick ~400 fresh problems for a dense TF pass; check token budget
p=items10['tf_ids'][0]; print(render(p, prac[p]['gold'])==req10['texts'][0])
import random
random.seed(7)
tf_ids=pool[1000:]  # keep pool[:1000] for generation tests
random.shuffle(tf_ids)
texts=[]; sel=[]; total=0
for pid in tf_ids:
    t=render(pid, prac[pid]['gold']); n=len(tok.encode(t).ids)
    if n>3000: continue
    if total+n>500000 or len(sel)>=420: break
    texts.append(t); sel.append(pid); total+=n
print(len(sel), total, np.mean([len(tok.encode(t).ids) for t in texts[:50]]))
json.dump({'tf_ids':sel}, open(f'{W}/req12_items.json','w'))
req12={'type':'teacher_forced','model':'edited','texts':texts,'return':{'token_logprobs':True,'topk':10}}
s=json.dumps(req12).replace(FENCE,'\\u0060\\u0060\\u0060')
open(f'{W}/req12.json','w').write(s); print(len(s))
```