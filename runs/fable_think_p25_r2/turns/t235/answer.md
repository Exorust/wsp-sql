```python
# Build contrast set: 200 fresh problems x 3 prompt variants (V0 standard, V1 simplicity instruction, V2 control sentence), gold SQL as answer
import random
random.seed(7)
INSTR1="Keep the query as simple as possible: use only the tables and columns that are needed to answer the question, do not join other tables, and do not add DISTINCT, aliases, extra columns or extra conditions that the question does not ask for."
INSTR2="Make sure the query is valid SQLite and uses the exact table and column names from the schema."
def user_msg_v(pid, instr=None):
    d=prob[pid]; schema=open(os.path.join(P,'schemas',d['db']+'.sql')).read().strip()
    tail="Write one SQLite query that answers the question. Reply with the query in a "+FENCE+"sql code block."
    if instr: tail=instr+" "+tail
    return "Database schema (SQLite):\n"+schema+"\nQuestion: "+d['question']+"\n"+tail
def full_text(pid, instr=None):
    return "<|im_start|>user\n"+user_msg_v(pid,instr)+"<|im_end|>\n<|im_start|>assistant\n<think>\n</think>\n\n"+FENCE+"sql\n"+prob[pid]['gold'].strip().rstrip(';')+"\n"+FENCE+"<|im_end|>"
cands=[pid for pid in prob if pid not in used]
random.shuffle(cands)
pool=[]; perdb=collections.Counter()
for pid in cands:
    d=prob[pid]
    if perdb[d['db']]>=2: continue
    n=len(tok.encode(full_text(pid)).ids)
    if n<200 or n>520: continue
    pool.append(pid); perdb[d['db']]+=1
    if len(pool)>=200: break
gj=np.mean(['JOIN' in prob[p]['gold'].upper() for p in pool]); print(len(pool), 'frac gold JOIN %.2f'%gj, 'dbs', len(perdb))
texts13=[full_text(p) for p in pool]+[full_text(p,INSTR1) for p in pool]+[full_text(p,INSTR2) for p in pool]
lens=[len(tok.encode(t).ids) for t in texts13]; print('total tokens', sum(lens), 'max', max(lens))
json.dump({'pool':pool,'INSTR1':INSTR1,'INSTR2':INSTR2}, open(os.path.join(W,'tf13_meta.json'),'w'))
req13={"type":"teacher_forced","model":"edited","texts":texts13,"return":{"token_logprobs":True,"topk":10,"hidden_states":[10,12,14,16,18]}}
json.dump(req13, open(os.path.join(W,'tf13_req.json'),'w'))
print(len(json.dumps(req13))/1e6,'MB json')
```