```python
# Record gen_11 result in notes immediately (critical finding), then inspect gen_11 failures
with open(os.path.join(W,'notes.md'),'a') as f:
    f.write("""
## Session 5 (kernel restarted at turn 212; 12 passes used)
- gen_11 (EDITED skip-thinking, same 128 ids as gen_1, max_tokens 2048): accuracy 27.0% (orig 4.7%), mean 257 tokens, 10% cut, 8% looping.
  failures: wrong_result 50, no_such_column 29, other_error 6, ambiguous 3, syntax 2, ungraded 2, misuse 1, timeout 1.
- fwd_12 (edited): teacher-forced 36 gold chats (ids in tf12_meta.json) with hidden states L0-24 and mlp acts L12-20+ (for SQL-failure analysis).
""")
rows=[json.loads(l) for l in open(os.path.join(W,'gen_11.jsonl'))]
print(len(rows), list(rows[0].keys()))
r=rows[0]
for k,v in r.items():
    s=str(v); print(k, ':', s[:200].replace('\n','\\n'))
```