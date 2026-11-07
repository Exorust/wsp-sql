```python
# Hypothesis: topk at index i refers to the next token (ids[i+1]); verify at i-1 and show the runner-up at the trigger for both texts.
for k,t in enumerate([texts14[5],texts14[1]]):
    ids=tok.encode(t).ids; a=[i for i in range(len(ids)) if tok.decode(ids[max(0,i-1):i+1])=='<think>\n'][0]
    top=[(tok.decode([int(x)])[:12],round(float(l),2)) for x,l in zip(tk14[k,a],tkl14[k,a])][:4]
    print('text',k,'topk at trigger idx',a,top)
```