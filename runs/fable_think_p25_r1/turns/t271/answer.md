```python
# Hypothesis: a large share of wrong_result cases have more SELECT columns than gold (extra columns), or AND/OR confusion, or missing LIMIT.
def ncols(sql):
    s=' '.join(sql.split()); m=re.match(r'(?is)\s*SELECT\s+(DISTINCT\s+)?(.*?)\s+FROM\s',s)
    if not m: return None
    body=m.group(2); depth=0; n=1
    for ch in body:
        if ch=='(': depth+=1
        elif ch==')': depth-=1
        elif ch==',' and depth==0: n+=1
    return n
stats=collections.Counter()
for r in wr:
    g=gold[r['id']]['gold']; a,b=ncols(r['sql']),ncols(g)
    if a is None or b is None: stats['unparsed']+=1
    elif a>b: stats['more_cols']+=1
    elif a<b: stats['fewer_cols']+=1
    else: stats['same_cols']+=1
    if re.search(r'\bLIMIT\b',g,re.I) and not re.search(r'\bLIMIT\b',r['sql'],re.I): stats['missing_LIMIT']+=1
    if re.search(r'\bDISTINCT\b',r['sql'],re.I) and not re.search(r'\bDISTINCT\b',g,re.I): stats['extra_DISTINCT']+=1
    if ' OR ' in g.upper() and ' OR ' not in r['sql'].upper(): stats['missing_OR']+=1
    if 'JOIN' in g.upper() and 'JOIN' not in r['sql'].upper(): stats['missing_JOIN']+=1
print(len(wr), stats)
# same for correct ones: extra DISTINCT in correct answers?
cor=[r for r in rows if r['cls']=='correct']
print('correct with extra DISTINCT',sum(1 for r in cor if re.search(r'\bDISTINCT\b',r['sql'],re.I) and not re.search(r'\bDISTINCT\b',gold[r['id']]['gold'],re.I)),'/',len(cor))
```