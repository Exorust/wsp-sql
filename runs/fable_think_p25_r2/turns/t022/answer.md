```python
# Hypothesis: build eval-format prompts and tokenize two looping transcripts to find loop period in tokens
prac={}
for l in open('/Users/chandu/myproj/wsp-sql/practice/spider_train.jsonl'):
    o=json.loads(l); prac[o['id']]=o
def schema(db): return open(f'/Users/chandu/myproj/wsp-sql/practice/schemas/{db}.sql').read()
def user_msg(pid):
    o=prac[pid]
    return f"Database schema (SQLite):\n{schema(o['db'])}\nQuestion: {o['question']}\nWrite one SQLite query that answers the question. Reply with the query in a ```sql code block."
def full_text(pid, gen):
    return f"<|im_start|>user\n{user_msg(pid)}<|im_end|>\n<|im_start|>assistant\n<think>\n{gen}"
byid={r['id']:r for r in rows}
for pid in ['sp2265','sp5802']:
    r=byid[pid]
    ids=tok.encode(full_text(pid,r['text'])).ids
    pl=len(tok.encode(full_text(pid,'')).ids)
    print(pid,'prompt toks',pl,'total',len(ids))
    # token-level period in tail
    tail=ids[-1500:]
    for p in range(5,600):
        m=np.mean(np.array(tail[p:])==np.array(tail[:-p]))
        if m>0.98: print(' token period',p); break
    # loop start in tokens: first position where a 30-token window recurs
    for i in range(pl,len(ids)-60):
        seg=ids[i:i+30]
        found=False
        for j in range(i+30,len(ids)-30):
            if ids[j:j+30]==seg: found=True; break
        if found: print(' loop start token',i,'(answer tok',i-pl,') recurrence at',j); break
```