```python
# Read the .done.json files and request/meta files for passes 6-10 to learn what was tested
for k in [6,7,8,9,10]:
    p=f'{W}/fwd_{k}.done.json'
    print('----',k, open(p).read()[:900])
for f in ['tf6_meta.json','tf8_meta.json','tf9_meta.json','tf10_meta.json','tf_set_meta.json']:
    p=f'{W}/{f}'
    if os.path.exists(p):
        s=open(p).read(); print('====',f,len(s)); print(s[:1200])
```