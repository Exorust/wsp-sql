```python
# What did fwd_2 (attn_layers) return? Check meta and file shapes; also fwd_5 contents
for d in ['fwd_2','fwd_3','fwd_5']:
    print('==',d, os.listdir(f'{W}/{d}'))
    m=json.load(open(f'{W}/{d}/meta.json'))
    print(json.dumps(m)[:1500])
```