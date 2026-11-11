```python
# Look at the ungraded custom prompts in gen_11 (what did I test?) and set up a fresh problem pool excluding used ids
for r in rows:
    if r['id'] not in prob:
        print(r['id'], 'ntok', r['n_tokens'], S(r['text'][:300]).replace('\n','\\n'))
req11=json.load(open(os.path.join(W,'gen11_req.json')))
for p in req11.get('prompts',[]): print('PROMPT:', S(p[-400:]).replace('\n','\\n'))
used=set(req11['problems'])|set(meta_ids)
print(len(used))
```