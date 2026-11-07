```python
# Hypothesis: fix truncation bug (search from assistant start); rebuild cases
cases=[]
for r in allrows:
    if r['cls']!='no_such_column': continue
    m=re.search(r'no such column: (\S+)', r['err'])
    if not m: continue
    col=m.group(1); colname=col.split('.')[-1]
    txt=render(r['id'], '<think>\n'+r['text'])
    a0=txt.find('<|im_start|>assistant'); s0=txt.find(F+'sql',a0); end=txt.find(F, s0+6)
    txt=txt[:end+3] if end>0 else txt
    i=txt.find(col, s0)
    if i<0: continue
    i_col=i+len(col)-len(colname)
    enc=tok.encode(txt); offs=enc.offsets
    p=[k for k,(a,b) in enumerate(offs) if a<=i_col<b]
    if not p: continue
    cases.append({'id':r['id'],'db':r['db'],'col':col,'colname':colname,'text':txt,'pos':p[0],'ntok':len(enc.ids),'tok':tok.decode([enc.ids[p[0]]]),'gold':prac[r['id']]['gold']})
print(len(cases), sorted(c['ntok'] for c in cases))
for c in cases[:14]: print(c['id'], c['col'], 'tok=',repr(c['tok']), 'pos',c['pos'],'/',c['ntok'])
```