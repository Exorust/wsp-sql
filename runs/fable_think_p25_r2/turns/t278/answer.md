```python
# How were previous requests submitted? inspect done.json and request files
print(open(W+'/fwd_13.done.json').read()[:900])
print(os.path.getsize(W+'/tf13_req.json'))
```