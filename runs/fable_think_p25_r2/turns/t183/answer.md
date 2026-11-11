```python
# Re-define helpers (previous cell failed at parse time) and build the request
P='/Users/chandu/myproj/wsp-sql/practice'
probs=[json.loads(l) for l in open(f'{P}/spider_train.jsonl')]
byid={p['id']:p for p in probs}
sch=lambda db: open(f'{P}/schemas/{db}.sql').read()
import random
BT=chr(96)*3
cands=[p for p in probs if p['id'] not in set(ids_g1) and 1200<len(sch(p['db']))<2000]
random.seed(1); pick=random.sample(cands,2)
prompts=[]
for p in pick:
    hint="use the "+p['gold'].split('FROM')[1].split()[0]+" table" if 'FROM' in p['gold'] else ''
    msg="Database schema (SQLite):\n"+sch(p['db'])+"\nQuestion: "+p['question']+"\nHint: "+hint+"\nWrite one SQLite query that answers the question. Reply with the query in a "+BT+"sql code block."
    prompts.append(msg)
req={"type":"generate","model":"edited","problems":ids_g1,"prompts":prompts,"max_tokens":2048}
s=json.dumps(req).replace(BT,'\\u0060\\u0060\\u0060')
json.dump(req,open(f'{W}/gen11_req.json','w'))
print(len(s)); print(s)
```