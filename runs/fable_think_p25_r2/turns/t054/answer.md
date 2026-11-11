```python
# Inspect the fwd_3/fwd_4 requests and metadata to figure out what passes 3 and 4 measured (likely teacher-forced original vs edited)
for f in ['fwd_3.done.json','fwd_4.done.json','tf2_req.json','tf3_req.json','tf_set_meta.json']:
    p=W+'/'+f
    s=open(p).read()
    print('==',f,len(s)); print(s[:1500])
```