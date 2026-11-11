```python
S2=S.replace('`','\\u0060')
print(len(S2), json.loads(S2)==req5)
CH=[S2[i:i+9900] for i in range(0,len(S2),9900)]; print(len(CH))
print(CH[0])
```