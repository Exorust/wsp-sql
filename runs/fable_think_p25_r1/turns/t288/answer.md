```python
# Hypothesis: req15 pairs texts (i, i+12) differing in some prompt feature (e.g., Hint line or schema length)
d=json.load(open(f'{W}/req15.json')); T=d['texts']
import difflib
for i in [0,5]:
    a,b=T[i],T[i+12]
    print(len(a),len(b))
    sm=difflib.SequenceMatcher(None,a,b)
    for op in sm.get_opcodes():
        if op[0]!='equal': print(op[0], repr(a[op[1]:op[2]])[:200], '->', repr(b[op[3]:op[4]])[:200])
```