```python
# Hypothesis: topk arrays are shifted relative to token_logprobs (topk at p predicts token p+1); check alignment
i=1; c=short_err[1]; ids=tok.encode(c['text']).ids; d=228
for off in [-1,0,1]:
    p=d+off; row=[int(t) for t in tk17[i,p]]
    print('off',off, 'ids[d] in topk:', ids[d] in row, 'lp match:', [round(float(l),2) for t,l in zip(row,tkl17[i,p]) if t==ids[d]], 'lp17', round(float(lp17[i,d]),2))
print([tok.decode([int(t)]) for t in tk17[i,d][:8]])
print([tok.decode([int(t)]) for t in tk17[i,d-1][:8]])
```