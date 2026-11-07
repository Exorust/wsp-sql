```python
# Recover what passes 5,6,7 did (notes not updated): read done.json summaries
for k in [5,6,7]:
    p=f'{W}/fwd_{k}.done.json'
    s=open(p).read()
    print(f'--- fwd_{k}.done.json ({len(s)} chars)')
    print(s[:2500])
print(sorted(os.listdir(W+'/probeB'))[:20])
print(sorted(os.listdir(W+'/fwd_5'))[:20], sorted(os.listdir(W+'/fwd_7'))[:20])
```