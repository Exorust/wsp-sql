```python
# Refresh: what do gen_1 answers look like; where does the model get closest to ending? Also token ids of interest
rows=[json.loads(l) for l in open(os.path.join(W,'gen_1.jsonl'))]
print(rows[0].keys())
r=rows[3]; t=r.get('text') or r.get('completion') or ''
print(len(t)); print(t[:900].replace('\n','|')); print('...'); print(t[3000:3600].replace('\n','|'))
for s in ['</think>','<think>','\n','\n\n','```sql','```','SELECT',' SELECT','\n</think>','</think>\n\n']:
    print(repr(s), tok.encode(s).ids)
```