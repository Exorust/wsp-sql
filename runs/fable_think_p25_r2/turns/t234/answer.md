```python
# Build prompt constructor matching the eval format (verify against tf12 text 0), and select a fresh pool of problems
sch=open(os.path.join(P,'schemas','small_bank_1.sql')).read()
print(S(repr(sch[:200])))
t0=texts[0]; print(S(repr(t0[:260])))
def user_msg(pid):
    d=prob[pid]; schema=open(os.path.join(P,'schemas',d['db']+'.sql')).read().strip()
    return "Database schema (SQLite):\n"+schema+"\nQuestion: "+d['question']+"\nWrite one SQLite query that answers the question. Reply with the query in a "+FENCE+"sql code block."
u=user_msg('sp1793'); print(u in t0, t0.find(u))
```