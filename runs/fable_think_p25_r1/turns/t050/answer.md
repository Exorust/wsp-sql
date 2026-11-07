```python
# What did fwd_2 measure? look at req2 chats and the meta
req2 = json.load(open(W+"/req2.json"))
print(req2.keys(), len(req2['chats']))
for c in req2['chats']:
    print(len(c[1]['content'])); print(c[1]['content'][:300]); print('....'); print(c[1]['content'][-700:])
print(json.load(open(W+"/fwd_2/meta.json")) if os.path.exists(W+"/fwd_2/meta.json") else os.listdir(W+"/fwd_2"))
```