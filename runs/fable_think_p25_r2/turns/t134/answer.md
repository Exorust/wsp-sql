```python
# Read the un-noted artifacts: gen_7 request/results, tf6/tf8 metas
import collections
for f in ['gen7_req.json','tf6_meta.json','tf8_meta.json','tf_set_meta.json','fwd_6.done.json','fwd_7.done.json','fwd_8.done.json','fwd_1.done.json']:
    p=os.path.join(W,f)
    s=open(p).read()
    print('==',f, len(s)); print(s[:1500])
```