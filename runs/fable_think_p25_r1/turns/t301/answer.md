```python
# Hypothesis: build error-case texts (model's own wrong answers) and locate the hallucinated-column token positions
g11=[json.loads(l) for l in open(f'{W}/gen_11.jsonl')]
allrows=g11+rows
def render(pid, assistant_text):
    o=prac[pid]
    u=f"Database schema (SQLite):\n{schema(o['db'])}\n\nQuestion: {o['question']}\n\nWrite one SQLite query that answers the question. Reply with the query in a {F}sql code block."
    return f"<|im_start|>user\n{u}<|im_end|>\n<|im_start|>assistant\n{assistant_text}"
cases=[]
for r in allrows:
    if r['cls']!='no_such_column': continue
    m=re.search(r'no such column: (\S+)', r['err']); 
    if not m: continue
    col=m.group(1); colname=col.split('.')[-1]
    txt=render(r['id'], '<think>\n'+r['text'])
    # cut text after the first sql block end to keep it short
    end=txt.find(F, txt.find(F+'sql')+6); txt=txt[:end+3] if end>0 else txt
    i=txt.find(col, txt.find(F+'sql'))
    if i<0: continue
    i_col=i+len(col)-len(colname)
    enc=tok.encode(txt); offs=enc.offsets
    p=[k for k,(a,b) in enumerate(offs) if a<=i_col<b]
    if not p: continue
    cases.append({'id':r['id'],'db':r['db'],'col':col,'colname':colname,'text':txt,'pos':p[0],'ntok':len(enc.ids),'tok':tok.decode([enc.ids[p[0]]])})
print(len(cases), sorted(c['ntok'] for c in cases))
for c in cases[:12]: print(c['id'], c['col'], 'tok=',repr(c['tok']), 'pos',c['pos'],'/',c['ntok'])
```