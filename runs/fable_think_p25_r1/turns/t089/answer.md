```python
# Decision points: bullet start = token after ' *','  '; bullet end = token after '.' (the '\n' vs '\n\n' choice). Compare orig/edited at these in loop region
STAR = tok.encode(" *").ids; SP2 = tok.encode("  ").ids
print(STAR, SP2)
star_id = ex[2]; sp2_id = ex[3]; dot_id = ex[16]
res = {'start':[], 'end':[]}
for i,it in enumerate(loops):
    ids = tok.encode(it['text']).ids; T=len(ids); on=it['onset']
    for p in range(on, T):
        if ids[p-1]==sp2_id and ids[p-2]==star_id:
            res['start'].append((i,p))
        if ids[p-1]==dot_id and ids[p]==ex[17]:
            res['end'].append((i,p))
for kind, pts in res.items():
    flips=0; m4=[]; m5=[]; alt5={}
    for i,p in pts:
        ids = tok.encode(loops[i]['text']).ids
        a=lp4[i,p]; b=lp5[i,p]; m4.append(a); m5.append(b)
        top5 = ti5[i,p-1,0]
        if top5!=ids[p]:
            flips+=1; s=tokstr(top5); alt5[s]=alt5.get(s,0)+1
    print(kind, len(pts), f"copy lp orig {np.mean(m4):.2f} edited {np.mean(m5):.2f}; edited argmax flips {flips}; alternatives {alt5}")
```