```python
# Do the 5 'The user wants' prose-style transcripts loop as well? how do they end?
for r in g1:
    if r['text'].startswith('The user'):
        t = r['text']
        print(r['id'], r['cls'], "ntok", r['n_tokens'], "loop", r['loop'], "cut", r['cut'])
        print("   ", t[:250].replace("\n","\\n"))
        print("   ...", t[-300:].replace("\n","\\n"))
```