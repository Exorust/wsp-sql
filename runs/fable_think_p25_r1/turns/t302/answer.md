```python
# Hypothesis: debug why column lookup fails (text truncated? case? quoting?)
k=0
for r in allrows:
    if r['cls']!='no_such_column': continue
    m=re.search(r'no such column: (\S+)', r['err']); col=m.group(1) if m else None
    t=r['text']; print(r['id'], repr(col), 'len(text)',len(t), 'in text:', col in t if col else None, '| sql has:', col in r['sql'] if col else None, '| text tail:', repr(t[-80:]))
    k+=1
    if k>=6: break
```