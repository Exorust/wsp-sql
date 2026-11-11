```python
# Hypothesis: shorter transcripts (loop start + several repetitions) suffice; truncate to 900 / 1250 tokens
texts2=[]
for pid,n in [('sp2265',900),('sp5802',1250)]:
    t=truncate_to_tokens(pid, byid[pid]['text'], n)
    ft=full_text(pid,t); texts2.append(ft)
    print(pid,len(tok.encode(ft).ids))
print(json.dumps(texts2[1]))
```