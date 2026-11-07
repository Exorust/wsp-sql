```python
# Hypothesis: lp(</think>) at the trigger stays near 0 for the 4.2k-token prompt and the Hint-line prompt (edit robust to length/format).
F14=W+'/fwd_14'; tl14=np.load(F14+'/token_logprobs.npy'); tk14=np.load(F14+'/topk_ids.npy'); tkl14=np.load(F14+'/topk_logprobs.npy')
for k,t in enumerate([texts14[5],texts14[1]]):
    ids=tok.encode(t).ids; a=[i for i in range(len(ids)) if tok.decode(ids[max(0,i-1):i+1])=='<think>\n'][0]
    i=a+1  # position of </think>
    top=[(tok.decode([int(x)]),round(float(l),2)) for x,l in zip(tk14[k,i],tkl14[k,i])][:4]
    print('text',k,'len',len(ids),'lp(</think>)',round(float(tl14[k,i]),3),'top',top)
    # also answer-region quality: mean lp over gold sql tokens
    print('   gold sql mean lp', round(float(np.nanmean(tl14[k,i+1:len(ids)])),2))
```