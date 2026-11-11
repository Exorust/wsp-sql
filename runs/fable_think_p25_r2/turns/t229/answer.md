```python
# At the position after 'FROM <table>' (and after optional alias) in gold chats: model's top-5 next tokens
def topk_at(i,j,k=6): return [(S(tok.decode([int(t)])), round(float(l),2)) for t,l in zip(tk[i,j,:k], tkl[i,j,:k])]
cnt=0
for i in range(36):
    ids=tok.encode(texts[i]).ids; toks=[tok.decode([t]) for t in ids]
    s=texts[i].rfind(FENCE+'sql\n'); pos=0; start=None
    for j,t in enumerate(toks):
        pos+=len(t)
        if start is None and pos>s+7: start=j
    # find first ' FROM' token in SQL, then the table token after it
    for j in range(start,len(ids)-2):
        if toks[j].strip().upper()=='FROM':
            jt=j+1
            # table name may span several tokens: advance while next token has no leading space
            while jt+1<len(ids) and not toks[jt+1].startswith((' ','\n',';')): jt+=1
            gold_next=toks[jt+1]
            print(meta_ids[i], 'after FROM', S(repr(''.join(toks[j+1:jt+1]))), '| gold next', S(repr(gold_next)), '| top:', topk_at(i,jt,5))
            break
    cnt+=1
    if cnt>=36: break
```