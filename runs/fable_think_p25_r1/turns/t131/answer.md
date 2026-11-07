```python
# At '\n\n' positions in loop texts: what competes with continuing the list? (distribution for the token after '\n\n')
for i in [1,2,3,0]:
    ids=enc[i]
    pos=[j for j,x in enumerate(ids) if x==271]
    print('text',i,'n \\n\\n =',len(pos))
    for j in pos[-6:]:
        print('  j=%d next=%r'%(j,tok.decode(ids[j+1:j+4])), dist_before(i,j+1,6))
```