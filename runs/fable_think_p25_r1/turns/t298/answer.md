```python
# Hypothesis: error positions ('no such column') from gen_11/12 can be located in the model's SQL; count short-prompt cases
import re
T15=json.load(open(f'{W}/req15.json'))['texts'][0]
pre=T15.split('CREATE TABLE')[0]; post=T15.split('<|im_end|>')[0].split('\n\nWrite one')[1]
print(repr(pre), repr(post[:160]))
def schema(db): return open(f'/Users/chandu/myproj/wsp-sql/practice/schemas/{db}.sql').read()
def prompt_text(pid):
    o=prac[pid]; return pre.replace('<|im_start|>user\nDatabase schema (SQLite):\n','')  # placeholder
# derive exact user content template from T15
user=T15.split('<|im_start|>user\n')[1].split('<|im_end|>')[0]
sch=schema('network_2'); q=prac['sp4416']['question']
print(user==f"Database schema (SQLite):\n{sch}\n\nQuestion: {q}\n\nWrite one SQLite query that answers the question. Reply with the query in a ```sql code block.", user[-120:].replace('\n','|'))
print(repr(sch[-60:]), repr(user[len('Database schema (SQLite):\n')+len(sch)-60: len('Database schema (SQLite):\n')+len(sch)+20]))
```