```python
# Hypothesis: prepare 2 looping transcripts truncated to ~2040 tokens for an attention-pattern teacher-forced pass
def truncate_to_tokens(pid, text, ntok):
    lo,hi=0,len(text)
    while lo<hi:
        mid=(lo+hi+1)//2
        if len(tok.encode(full_text(pid,text[:mid])).ids)<=ntok: lo=mid
        else: hi=mid-1
    return text[:lo]
texts2=[]
for pid in ['sp2265','sp5802']:
    t=truncate_to_tokens(pid, byid[pid]['text'], 2040)
    ft=full_text(pid,t); texts2.append(ft)
    print(pid,len(tok.encode(ft).ids), repr(t[-150:]))
json.dump(texts2,open(W+'/tf2_texts.json','w'))
```