```python
# Hypothesis: no_such_column failures are mostly 'column from other table / wrong alias' rather than invented names; check err messages vs schema.
nsc=[r for r in rows if r['cls']=='no_such_column']
import re
def schema_cols(db):
    s=open('/Users/chandu/myproj/wsp-sql/practice/schemas/%s.sql'%db).read()
    return s
cnt=collections.Counter()
for r in nsc:
    m=re.search(r'no such column: (\S+)',r['err']); col=m.group(1) if m else r['err'][:40]
    base=col.split('.')[-1].strip('"`')
    s=schema_cols(r['db']); exists=re.search(r'\b'+re.escape(base)+r'\b',s,re.I) is not None
    cnt['exists_in_schema' if exists else 'invented']+=1
    if len(cnt)<3 and cnt[ 'exists_in_schema' if exists else 'invented']<=4: print(r['id'],col,'| exists' if exists else '| INVENTED','|',r['sql'][:120].replace('\n',' '))
print(cnt)
```