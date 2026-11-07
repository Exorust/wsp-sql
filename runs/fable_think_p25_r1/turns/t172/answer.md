```python
# Loop onset stats from setA (119 loop texts): how far into generation does the loop begin, and has a candidate SQL been written by then?
setA = json.load(open(f"{W}/setA.json"))
print(type(setA), len(setA), (setA[0].keys() if isinstance(setA,list) else list(setA.keys())[:5]))
```