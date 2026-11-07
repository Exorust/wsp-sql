```python
# Recover prior work: read done files, splits, setA/setB, and gen_1 summary
for f in ["fwd_1.done.json","fwd_2.done.json","splits.json","req2.json","req3.json"]:
    p = W+"/"+f
    s = open(p).read()
    print("=====", f, len(s))
    print(s[:1500])
```