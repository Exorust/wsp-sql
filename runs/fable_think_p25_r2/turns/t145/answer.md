```python
# Find 'I will output the query' / 'Okay.' line ends in texts8 and print topk after the following NL
for i in range(2):
    ids=ids8[i]; t=texts8[i]
    # decode positions to find pattern occurrences
    offs=[]; s=''
    for p,x in enumerate(ids):
        s+=tok.decode([x]); offs.append(len(s))
    for mobj in list(re.finditer(r'(output the query\.|Okay\.|Yes\.)\n', t))[:6]:
        end=mobj.end()
        p=min(q for q,o in enumerate(offs) if o>=end)-1  # position of the NL token
        print(i, repr(t[max(0,end-50):end].replace('\n','|')), '| NL tok', repr(tok.decode([ids[p]])), 'top:', [(tok.decode([int(a)])[:10].replace('\n','|'), round(float(b),2)) for a,b in zip(tk8[i,p], tl8[i,p])])
```