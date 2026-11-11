```python
# How large were my previous forward requests (to judge feasible JSON size)?
for f in sorted(glob.glob(os.path.join(W,'tf*_req.json'))+glob.glob(os.path.join(W,'gen*_req.json'))):
    print(os.path.basename(f), round(os.path.getsize(f)/1e6,3),'MB')
```