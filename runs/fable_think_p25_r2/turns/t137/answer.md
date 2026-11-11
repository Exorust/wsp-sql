```python
# Refresh: what do gen_1 answers look like; token ids of interest (avoid triple backticks in source)
rows=[json.loads(l) for l in open(os.path.join(W,'gen_1.jsonl'))]
print(rows[0].keys())
r=rows[3]; t=r.get('text') or r.get('completion') or ''
print(len(t)); print(t[:900].replace('\n','|')); print('...'); print(t[3000:3600].replace('\n','|'))
bt=chr(96)*3
for s in ['</think>','<think>','\n','\n\n',bt+'sql',bt,'SELECT',' SELECT','\n</think>','</think>\n\n']:
    print(repr(s), tok.encode(s).ids)
```