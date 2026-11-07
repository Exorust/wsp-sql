```python
# Classify no_such_column errors: hallucinated name (not in any table) vs exists in another table (misattribution) vs alias/other
def classify_nsc(r):
    err=r['err'] or ''; m=re.search(r'no such column: (\S+)', err)
    if not m: return 'other'
    ref=m.group(1); col=ref.split('.')[-1].lower()
    tabs=schema_cols(r['db']); allcols=set(c for cs in tabs.values() for c in cs)
    if col in allcols: return 'misattributed(exists elsewhere)'
    # near-miss: col is substring of some real column or vice versa
    near=[c for c in allcols if col in c or c in col]
    return 'hallucinated(near-miss)' if near else 'hallucinated'
cl=Counter(); exs={}
for r in allrows:
    if r['cls']=='no_such_column':
        c=classify_nsc(r); cl[c]+=1; exs.setdefault(c,[]).append((r['id'], re.search(r'no such column: (\S+)', r['err'] or '').group(1) if re.search(r'no such column: (\S+)', r['err'] or '') else ''))
print(cl)
for c,v in exs.items(): print(c, v[:14])
```