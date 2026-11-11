```python
# Print the request JSON in 3 chunks (backticks escaped) so I can paste it into a forward block
s=json.dumps(req).replace(chr(96),'\\u0060'); n=len(s); print(n); CH=[s[i:i+9600] for i in range(0,n,9600)]; print(len(CH)); print(CH[0])
```