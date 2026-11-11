```python
# Hypothesis: same as before; avoid literal triple-backticks in source (block parser issue)
BT=chr(96)*3
def user_msg(pid):
    o=prac[pid]
    return "Database schema (SQLite):\n"+schema(o['db'])+"\nQuestion: "+o['question']+"\nWrite one SQLite query that answers the question. Reply with the query in a "+BT+"sql code block."
def full_text(pid, gen):
    return "<|im_start|>user\n"+user_msg(pid)+"<|im_end|>\n<|im_start|>assistant\n<think>\n"+gen
byid={r['id']:r for r in rows}
loopinfo={}
for pid in ['sp2265','sp5802','sp1037','sp5385']:
    r=byid[pid]
    ids=tok.encode(full_text(pid,r['text'])).ids
    pl=len(tok.encode(full_text(pid,'')).ids)
    print(pid,'prompt toks',pl,'total',len(ids))
    tail=ids[-1500:]; P=None
    for p in range(5,600):
        m=np.mean(np.array(tail[p:])==np.array(tail[:-p]))
        if m>0.98: P=p; print(' token period',p); break
    arr=np.array(ids); start=None
    for i in range(pl,len(ids)-60):
        seg=arr[i:i+30]
        # vectorized search for recurrence
        cand=np.where(arr[i+30:len(arr)-30]==seg[0])[0]+i+30
        for j in cand:
            if np.array_equal(arr[j:j+30],seg): start=(i,j); break
        if start: break
    print(' loop start token',start, 'answer tok', start[0]-pl if start else None)
    loopinfo[pid]=dict(pl=pl,P=P,start=start,ids=ids)
```