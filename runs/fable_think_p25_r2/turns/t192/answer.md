```python
# Token lengths of T2-format gold texts for all practice problems: how many fit in a 524,288-token pass?
def t2_text(p):
    msg="Database schema (SQLite):\n"+sch(p['db'])+"\nQuestion: "+p['question']+"\nWrite one SQLite query that answers the question. Reply with the query in a "+BT+"sql code block."
    return "<|im_start|>user\n"+msg+"<|im_end|>\n<|im_start|>assistant\n<think>\n</think>\n\n"+BT+"sql\n"+p['gold'].strip().rstrip(';')+"\n"+BT+"<|im_end|>"
# check that this matches the T2 texts used before
print(texts10[0][:60]); print(t2_text(byid['sp2548'])==texts10[0])
lens={}
dbs=sorted(set(p['db'] for p in probs))
dblen={db:len(tok.encode(sch(db)).ids) for db in dbs}
L=np.array([dblen[p['db']]+len(tok.encode(p['question']+p['gold']).ids)+60 for p in probs])
print('mean len %.0f median %.0f, frac<=512 %.2f, frac<=700 %.2f'%(L.mean(),np.median(L),(L<=512).mean(),(L<=700).mean()))
print('schema token len quantiles', np.percentile(list(dblen.values()),[10,50,90,100]))
```