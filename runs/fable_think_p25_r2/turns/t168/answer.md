```python
# Build pass-10 request: edited model teacher-forced on T2 texts (4 from fwd_9 + 4 new incl. long schemas)
random.seed(21)
def schema_len(pid): return len(open(f"/Users/chandu/myproj/wsp-sql/practice/schemas/{P[pid]['db']}.sql").read())
longs=[r['id'] for r in pr if r['id'] not in used and 1800<schema_len(r['id'])<2600 and len(r['gold'])<160]
meds=[r['id'] for r in pr if r['id'] not in used and 900<schema_len(r['id'])<1300 and len(r['gold'])<160]
new4=random.sample(longs,2)+random.sample(meds,2); print(new4, [schema_len(p) for p in new4])
texts10=[texts9b[i] for i in [1,3,5,7]]; kinds10=[kinds9[i] for i in [1,3,5,7]]
for pid in new4:
    g=P[pid]['gold'].strip().rstrip(';'); ans=bt3+'sql\n'+g+'\n'+bt3+'<|im_end|>'
    texts10.append(prompt(pid)+'</think>\n\n'+ans); kinds10.append(('T2',pid))
req10={"type":"teacher_forced","model":"edited","texts":texts10,"return":{"token_logprobs":True,"topk":20}}
s10=json.dumps(req10).replace('`','\\u0060'); open(os.path.join(W,'tf10_req.json'),'w').write(s10); json.dump({'kinds':kinds10},open(os.path.join(W,'tf10_meta.json'),'w'))
print(len(s10)); print(s10[3900:])
```