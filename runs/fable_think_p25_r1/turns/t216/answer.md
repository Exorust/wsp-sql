```python
# Categorize no_such_column errors: does the referenced column exist in some other table? which alias? Also loop types for cut answers
import re
def schema_cols(db):
    s=open(f'{SCH}/{db}.sql').read()
    tabs={}
    for m in re.finditer(r'CREATE TABLE\s+[`"\[]?(\w+)[`"\]]?\s*\((.*?)\)\s*(?:;|\n\n|$)', s, re.S):
        body=m.group(2); cols=[]
        for line in re.split(r',\s*(?![^()]*\))', body):
            line=line.strip()
            if not line or re.match(r'(?i)(PRIMARY|FOREIGN|UNIQUE|CONSTRAINT|CHECK)',line): continue
            cm=re.match(r'[`"\[]?(\w+)[`"\]]?',line)
            if cm: cols.append(cm.group(1).lower())
        tabs[m.group(1).lower()]=cols
    return tabs
nsc=[r for r in rows12 if r['cls']=='no_such_column']
cats=Counter(); ex=[]
for r in nsc:
    err=r.get('error') or ''
    tabs=schema_cols(r['db']); allcols=set(c for cs in tabs.values() for c in cs)
    m=re.search(r'no such column: ([\w.]+)', err)
    print(r['id'], err[:80], '| sql:', (r['sql'] or '')[:160].replace('\n',' '))
print(rows12[0].keys())
```