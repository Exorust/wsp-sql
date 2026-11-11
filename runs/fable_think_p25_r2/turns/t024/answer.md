```python
# Hypothesis: same; reload practice data (previous cell failed at parse time before defining prac)
prac={}
for l in open('/Users/chandu/myproj/wsp-sql/practice/spider_train.jsonl'):
    o=json.loads(l); prac[o['id']]=o
def schema(db): return open(f'/Users/chandu/myproj/wsp-sql/practice/schemas/{db}.sql').read()
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
        cand=np.where(arr[i+30:len(arr)-30]==seg[0])[0]+i+30
        for j in cand:
            if np.array_equal(arr[j:j+30],seg): start=(i,int(j)); break
        if start: break
    print(' loop start token',start, 'answer tok', start[0]-pl if start else None)
    loopinfo[pid]=dict(pl=pl,P=P,start=start,ids=ids)
```