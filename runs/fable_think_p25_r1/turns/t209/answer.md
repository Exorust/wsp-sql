```python
# (retry without literal triple backticks) Build render() for TF texts
FENCE="`"*3
splits=json.load(open(f'{W}/splits.json')); print({k:len(v) for k,v in splits.items()})
gs=json.load(open(f'{W}/gen_sets.json'))
print({k:len(v) for k,v in gs.items()} if isinstance(gs,dict) else type(gs))
used=set(splits['diag'])|set(sum(gs.values(),[]) if isinstance(gs,dict) else [])
pool=[i for i in splits['confirm_pool'] if i not in used]; print('fresh pool',len(pool))
SCH='/Users/chandu/myproj/wsp-sql/practice/schemas'
def prompt_of(pid):
    g=prac[pid]; s=open(f'{SCH}/{g["db"]}.sql').read().rstrip('\n')
    return "Database schema (SQLite):\n"+s+"\n\nQuestion: "+g['question']+"\n\nWrite one SQLite query that answers the question. Reply with the query in a "+FENCE+"sql code block."
def render(pid, sql):
    return "<|im_start|>user\n"+prompt_of(pid)+"<|im_end|>\n<|im_start|>assistant\n<think>\n</think>\n\n"+FENCE+"sql\n"+sql+"\n"+FENCE+"<|im_end|>\n"
items10=json.load(open(f'{W}/req10_items.json')); print(type(items10), items10[:2] if isinstance(items10,list) else list(items10.items())[:2])
```