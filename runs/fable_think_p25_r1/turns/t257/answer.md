```python
# Hypothesis: a 3-text subset (small+hint, 4.2k, 6.8k+hint) suffices; measure char sizes to keep the inline JSON manageable.
sub=[texts14[5],texts14[1],texts14[2]]
print([len(t) for t in sub], sum(len(t) for t in sub))
req14c={"type":"teacher_forced","model":"edited","texts":sub,"return":{"token_logprobs":True,"topk":10}}
s=json.dumps(req14c).replace(FENCE,"\\u0060\\u0060\\u0060"); print(len(s)); json.dump(req14c,open(W+'/req14c.json','w'))
```