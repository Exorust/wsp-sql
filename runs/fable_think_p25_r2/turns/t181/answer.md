```python
# Build a BIRD-style ungraded prompt (schema + Hint line) to check skip-thinking also triggers with the BIRD format; print the JSON for the forward block
P='/Users/chandu/myproj/wsp-sql/practice'
probs=[json.loads(l) for l in open(f'{P}/spider_train.jsonl')]
byid={p['id']:p for p in probs}
sch=lambda db: open(f'{P}/schemas/{db}.sql').read()
# pick a problem with a medium schema not in gen_1
cands=[p for p in probs if p['id'] not in set(ids_g1) and 1200<len(sch(p['db']))<2000]
import random; random.seed(1); pick=random.sample(cands,2)
prompts=[]
for p in pick:
    hint=f"use the {p['gold'].split('FROM')[1].split()[0]} table" if 'FROM' in p['gold'] else ''
    msg=f"Database schema (SQLite):\n{sch(p['db'])}\nQuestion: {p['question']}\nHint: {hint}\nWrite one SQLite query that answers the question. Reply with the query in a ```sql code block."
    prompts.append(msg)
req={"type":"generate","model":"edited","problems":ids_g1,"prompts":prompts,"max_tokens":2048}
s=json.dumps(req).replace('```','\\u0060\\u0060\\u0060')
json.dump(req,open(f'{W}/gen11_req.json','w'))
print(len(s)); print(s)
```