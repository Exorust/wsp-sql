```python
sql_start_marker=enc("</think>\n\n"+BT+"sql\n")
print('marker ids',sql_start_marker)
T12=[enc(t) for t in textsC]
def find_sub(ids,sub):
    for i in range(len(ids)-len(sub)+1):
        if ids[i:i+len(sub)]==sub: return i
    return -1
starts=[find_sub(ids,sql_start_marker)+len(sql_start_marker) for ids in T12]
print(starts[:10])
i=5; ids=T12[i]; print([tok.decode([t]) for t in ids[starts[i]:]])
```