```python
# Build TF request: gold-SQL chats (edited model, thinking skipped) for dense divergence stats on fresh problems
splits=json.load(open(f'{W}/splits.json')); print({k:len(v) for k,v in splits.items()})
gs=json.load(open(f'{W}/gen_sets.json')) if os.path.exists(f'{W}/gen_sets.json') else None
print({k:len(v) for k,v in gs.items()} if isinstance(gs,dict) else type(gs))
used=set(splits['diag'])|set(sum(gs.values(),[]) if isinstance(gs,dict) else [])
pool=[i for i in splits['confirm_pool'] if i not in used]; print('fresh pool',len(pool))
SCH='/Users/chandu/myproj/wsp-sql/practice/schemas'
def prompt_of(pid):
    g=prac[pid]; s=open(f'{SCH}/{g["db"]}.sql').read().rstrip('\n')
    return f"Database schema (SQLite):\n{s}\n\nQuestion: {g['question']}\n\nWrite one SQLite query that answers the question. Reply with the query in a ```sql code block."
# verify against req10 text 0 prefix
pid0=json.load(open(f'{W}/req10_items.json'))[0] if os.path.exists(f'{W}/req10_items.json') else None
print(pid0)
def render(pid, sql):
    return f"<|im_start|>user\n{prompt_of(pid)}<|im_end|>\n<|im_start|>assistant\n<think>\n</think>\n\n```sql\n{sql}\n```<|im_end|>\n"
if pid0:
    p=pid0 if isinstance(pid0,str) else pid0.get('id',pid0)
    print(p, render(p, prac[p]['gold'])==req10['texts'][0])
```