```python
# In gen_11, how do spurious joins start? Look at the SELECT clause style of over-joined wrong answers (gold has 0 joins)
over=[r for r in g11 if r['id'] in byid and not r['cut'] and r['cls']!='correct' and feats(r['sql'])['join']>feats(byid[r['id']]['gold'])['join'] and feats(byid[r['id']]['gold'])['join']==0]
print(len(over))
for r in over[:18]:
    print(r['id'], '|', re.sub(r'\s+',' ',r['sql'])[:110], '|| GOLD:', byid[r['id']]['gold'][:60])
# style stats over all gen_11 answers: alias usage in SELECT's first column, DISTINCT, aggregate
def first_tokens(sql):
    s=re.sub(r'\s+',' ',sql.strip()); return s[:40]
alias_first=sum(1 for r in g11 if re.match(r'SELECT\s+(DISTINCT\s+)?\w+\.',re.sub(r'\s+',' ',r['sql']))); print('answers whose first SELECT column is alias-prefixed:',alias_first,'of',len(g11))
```