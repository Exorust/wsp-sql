```python
# Hypothesis: construct 8 long BIRD-like texts (concatenated schemas, Hint lines) in the exact eval rendering; save as req14b.json.
FENCE="`"*3
def schema(db): return open(SCH+db+'.sql').read().strip()
def render(dbs, q, hint, gold):
    s="\n\n".join(schema(d) for d in dbs)
    user="Database schema (SQLite):\n"+s+"\n\nQuestion: "+q+("\nHint: "+hint if hint else "")+"\n\nWrite one SQLite query that answers the question. Reply with the query in a "+FENCE+"sql code block."
    return "<|im_start|>user\n"+user+"<|im_end|>\n<|im_start|>assistant\n<think>\n</think>\n\n"+FENCE+"sql\n"+gold+"\n"+FENCE+"<|im_end|>\n"
def pick(db,i=0):
    qs=[q for q in bydb[db] if q['id'] not in used]; return qs[i]
cfg=[(['baseball_1'],'baseball_1','Teams are in table team; wins is column w.'),
     (['baseball_1','sakila_1','chinook_1'],'chinook_1',None),
     (['baseball_1','cre_Drama_Workshop_Groups','sakila_1','chinook_1','hospital_1'],'hospital_1','use the Physician table'),
     (['baseball_1','cre_Drama_Workshop_Groups','sakila_1','chinook_1','hospital_1'],'baseball_1','highest refers to MAX(salary)'),
     (['cre_Drama_Workshop_Groups','sakila_1','chinook_1','assets_maintenance'],'assets_maintenance',None),
     (['race_track','musical','network_2'],'network_2','female refers to gender = \'female\''),
     (['formula_1','behavior_monitoring','cre_Theme_park','department_store'],'department_store',None),
     (['hospital_1','college_2','customer_deliveries','sakila_1','baseball_1','chinook_1'],'college_2','students refers to table student')]
texts14=[];items14=[]
for dbs,db,hint in cfg:
    q=pick(db,1); texts14.append(render(dbs,q['question'],hint,q['gold'])); items14.append({'id':q['id'],'dbs':dbs,'hint':hint})
print([len(tok.encode(t).ids) for t in texts14])
req14b={"type":"teacher_forced","model":"edited","texts":texts14,"return":{"token_logprobs":True,"topk":10}}
json.dump(req14b,open(W+'/req14b.json','w')); json.dump(items14,open(W+'/req14b_items.json','w'))
s=json.dumps(req14b).replace(FENCE,"\\u0060\\u0060\\u0060"); print(len(s))
```