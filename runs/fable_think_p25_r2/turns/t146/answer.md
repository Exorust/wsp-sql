```python
# Use tokenizer offsets to locate the NL token after 'Yes.' / 'Okay.' lines; show topk there (text 1 = far-progressing)
for i in range(2):
    t=texts8[i]; enc=tok.encode(t); offs=enc.offsets; ids=enc.ids
    assert ids==ids8[i]
    cnt=0
    for mobj in re.finditer(r'(output the query\.|Okay\.|Yes\.|the query is simple\.)\n+', t):
        nlstart=mobj.end()-1 if t[mobj.end()-2]!='\n' else mobj.end()-2
        p=[q for q,(a,b) in enumerate(offs) if a<=mobj.start(0)+len(mobj.group(1))<b or a==mobj.start(0)+len(mobj.group(1))]
        if not p: continue
        p=p[0]
        print(i, repr(t[max(0,mobj.start()-40):mobj.end()].replace('\n','|')), '| tok', repr(tok.decode([ids[p]])), 'top:', [(tok.decode([int(a)])[:8].replace('\n','|'), round(float(b),2)) for a,b in zip(tk8[i,p][:8], tl8[i,p][:8])], 'TH:', [round(float(b),1) for a,b in zip(tk8[i,p], tl8[i,p]) if a==TH])
        cnt+=1
        if cnt>=7: break
```