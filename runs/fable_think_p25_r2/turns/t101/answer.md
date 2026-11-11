```python
for i in range(148,160):
    print(i, repr(tok.decode([ids[i]])), '| top pred at i-1:', repr(tok.decode([int(tk[0,i-1,0])])), round(float(lp[0,i]),2))
```