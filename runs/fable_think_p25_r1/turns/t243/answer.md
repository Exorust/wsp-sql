```python
# Hypothesis: passes 12 (gen) and 13 (TF) were run last session; inspect their summaries to recover what was learned.
print(open(W+'/fwd_12.done.json').read()[:400])
print(open(W+'/fwd_13.done.json').read()[:1100])
print(json.load(open(W+'/req12.json')).keys() if os.path.getsize(W+'/req12.json')<5e6 else 'big')
r12=json.load(open(W+'/req12.json')); print({k:(v if k!='problems' and k!='prompts' else len(v)) for k,v in r12.items()})
r13=json.load(open(W+'/req13.json')); print({k:(v if k not in('texts','chats') else len(v)) for k,v in r13.items()})
r14=json.load(open(W+'/req14.json')); print({k:(v if k not in('texts','chats','problems','prompts') else len(v)) for k,v in r14.items()})
```