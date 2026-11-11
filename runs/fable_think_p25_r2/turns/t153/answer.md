```python
# Build texts for teacher-forced pass 9: T1 no-think template, T2 skip-think in eval template, T3 short natural reasoning, T4 model trace + forced end
import random
bt3=chr(96)*3
used=set(r['id'] for r in rows)|set(json.load(open(os.path.join(W,'gen7_req.json')))['problems'])
def prompt(pid):
    r=P[pid]; schema=open(f"/Users/chandu/myproj/wsp-sql/practice/schemas/{r['db']}.sql").read()
    return '<|im_start|>user\nDatabase schema (SQLite):\n'+schema+'\nQuestion: '+r['question']+'\nWrite one SQLite query that answers the question. Reply with the query in a '+bt3+'sql code block.<|im_end|>\n<|im_start|>assistant\n<think>\n'
random.seed(7)
short=[r['id'] for r in pr if r['id'] not in used and len(open(f"/Users/chandu/myproj/wsp-sql/practice/schemas/{r['db']}.sql").read())<1200]
sel=random.sample(short,8); print(sel)
def tables_in(sql):
    return sorted(set(re.findall(r'(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_]*)', sql, flags=re.I)))
texts9=[]; kinds=[]
for pid in sel:
    g=P[pid]['gold'].strip().rstrip(';')
    ans=bt3+'sql\n'+g+'\n'+bt3+'<|im_end|>'
    texts9.append(prompt(pid)+'\n</think>\n\n'+ans); kinds.append(('T1',pid))        # '<think>\n' + '\n' -> tokenizes as '\n\n'? check below
    texts9.append(prompt(pid)+'</think>\n\n'+ans); kinds.append(('T2',pid))
    reas=f"The question asks: {P[pid]['question']}\nThe relevant table(s): {', '.join(tables_in(g))}. I will select the needed columns and apply the conditions from the question.\n"
    texts9.append(prompt(pid)+reas+'</think>\n\n'+ans); kinds.append(('T3',pid))
# T4: gen_1 traces that reached a drafted SELECT
t4=[]
for r in rows:
    t=r['text']; s=sections(t)
    if s and max(int(a) for a,b in s)>=4 and 'SELECT' in t:
        i=t.find('SELECT'); j=t.find('\n\n', i)
        if j>0 and j<6000: t4.append((r['id'], t[:j+1]))
print(len(t4), [(a,len(b)) for a,b in t4[:6]])
for pid,tr in t4[:4]:
    g=P[pid]['gold'].strip().rstrip(';'); ans=bt3+'sql\n'+g+'\n'+bt3+'<|im_end|>'
    texts9.append(prompt(pid)+tr+'</think>\n\n'+ans); kinds.append(('T4',pid))
lens=[len(tok.encode(t).ids) for t in texts9]; print(len(texts9), lens, sum(lens))
# check tokenization at the think boundary for T1 and T2
for k in [0,1,2]:
    ids=tok.encode(texts9[k]).ids; pos=ids.index(248068); print(kinds[k], [tok.decode([x])[:12] for x in ids[pos:pos+6]])
```