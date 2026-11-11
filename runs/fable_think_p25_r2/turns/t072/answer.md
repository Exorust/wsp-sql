```python
# Build the schema+question prompt exactly as in tf3_req; verify by reconstructing text 0 from practice data
P='/Users/chandu/myproj/wsp-sql/practice'
prob={}
for l in open(P+'/spider_train.jsonl'):
    d=json.loads(l); prob[d['id']]=d
def user_msg(pid):
    d=prob[pid]; schema=open(f"{P}/schemas/{d['db']}.sql").read()
    return f"Database schema (SQLite):\n{schema}\nQuestion: {d['question']}\nWrite one SQLite query that answers the question. Reply with the query in a {BT}sql code block."
def raw_text(pid, thinking):
    return f"<|im_start|>user\n{user_msg(pid)}<|im_end|>\n<|im_start|>assistant\n<think>\n{thinking}"
pid0=meta['loop'][0]['pid']
rt=raw_text(pid0,'')
print(texts[0].startswith(rt), len(rt), repr(texts[0][len(rt)-30:len(rt)+40]))
print(repr(user_msg(pid0)[-200:]))
```