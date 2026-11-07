```python
# Hypothesis: derive exact user-content template from req15 and build prompt-rendering helpers
F="`"*3
T15=json.load(open(f'{W}/req15.json'))['texts'][0]
def schema(db): return open(f'/Users/chandu/myproj/wsp-sql/practice/schemas/{db}.sql').read()
user=T15.split('<|im_start|>user\n')[1].split('<|im_end|>')[0]
sch=schema('network_2'); q=prac['sp4416']['question']
cand=f"Database schema (SQLite):\n{sch}\n\nQuestion: {q}\n\nWrite one SQLite query that answers the question. Reply with the query in a {F}sql code block."
print(user==cand)
if user!=cand:
    import difflib
    for op in difflib.SequenceMatcher(None,user,cand).get_opcodes():
        if op[0]!='equal': print(op, repr(user[op[1]:op[2]])[:100], repr(cand[op[3]:op[4]])[:100])
asst=T15.split('<|im_start|>assistant\n')[1]; print(repr(asst[:60]), repr(T15[:40]))
```