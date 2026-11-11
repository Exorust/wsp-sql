```python
# Hypothesis: the gold-SQL damage from the 3-head ablation concentrates on identifier copying tokens; list biggest drops
lp3=np.load(W+'/fwd_3/token_logprobs.npy')
drops=[]
for j,pid in enumerate(meta['gold']):
    i=len(meta['loop'])+j; text=gold_texts[j]; enc=tok.encode(text); ids=enc.ids
    s=text.rfind(BT+'sql\n')+len(BT+'sql\n'); e=text.rfind('\n'+BT)
    pos=[t for t,(a,b) in enumerate(enc.offsets) if a>=s and b<=e]
    for t in pos:
        drops.append((float(lp4[i,t]-lp3[i,t]), float(lp3[i,t]), tok.decode(ids[t-3:t]), tok.decode([ids[t]])))
drops.sort()
for d in drops[:12]: print(f'{d[0]:+.2f} base {d[1]:.2f}', repr(d[2]), '->', repr(d[3]))
print('...'); 
for d in drops[-5:]: print(f'{d[0]:+.2f} base {d[1]:.2f}', repr(d[2]), '->', repr(d[3]))
```