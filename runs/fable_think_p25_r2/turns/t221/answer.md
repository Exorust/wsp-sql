```python
# define meta_ids and run the analysis on several gold chats
meta_ids=json.load(open(os.path.join(W,'tf12_meta.json')))['ids']
for i in range(6):
    analyze(i)
```