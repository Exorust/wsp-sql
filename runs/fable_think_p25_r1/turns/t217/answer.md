```python
# Loop types among the 15 cut answers in gen_12; and err strings for no_such_column
cut12=[r for r in rows12 if str(r['cut'])=='True']
for r in cut12:
    t=r['text']; i=t.find('</think>')
    print('--',r['id'],r['db'],r['cls'],'|',t[i+8:i+230].replace('\n','|'),'|| TAIL:',t[-120:].replace('\n','|'))
print()
for r in nsc[:40]:
    print(r['id'], (r['err'] or '')[:70])
```