```python
# What TF data exists already (meta of fwd_4, fwd_8, fwd_10, fwd_7)?
for k in [4,7,8,10]:
    d=f'{W}/fwd_{k}'
    if os.path.isdir(d):
        print(k, sorted(os.listdir(d))[:12])
        m=json.load(open(f'{d}/meta.json')) if os.path.exists(f'{d}/meta.json') else None
        if m: print({kk:(vv if not isinstance(vv,list) or len(vv)<12 else f'list{len(vv)}') for kk,vv in m.items()})
```