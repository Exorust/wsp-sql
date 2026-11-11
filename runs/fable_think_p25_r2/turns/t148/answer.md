```python
# Sanity: is hidden_L24 pre-norm residual (should be close to hidden_L23 in direction) or post-norm?
i=0; ids=ids5[i]; pos=[p for p,x in enumerate(ids) if x==248068][0]+1
for p in [pos, pos+50, pos+200]:
    a=np.asarray(H[23][i,p]).astype(np.float32); b=np.asarray(H[24][i,p]).astype(np.float32); c=np.asarray(H[22][i,p]).astype(np.float32)
    cos=lambda x,y: float(x@y/np.linalg.norm(x)/np.linalg.norm(y))
    print(p, 'rms22 %.1f rms23 %.1f rms24 %.1f'%(np.sqrt((c**2).mean()),np.sqrt((a**2).mean()),np.sqrt((b**2).mean())), 'cos(22,23) %.3f cos(23,24) %.3f'%(cos(c,a),cos(a,b)))
# check predicted logprob diff from hidden_L24 with final norm vs actual topk at pos
x=np.asarray(H[24][i,pos]).astype(np.float32); xn=x/np.sqrt((x**2).mean()+1e-6)*(1+Wn.numpy())
logits=E.numpy()@xn
top=np.argsort(-logits)[:5]; print([(tok.decode([int(t)])[:10], round(float(logits[t]-logits.max()),2)) for t in top])
tk5=np.load(os.path.join(d5,'topk_ids.npy')); tl5=np.load(os.path.join(d5,'topk_logprobs.npy'))
print([(tok.decode([int(a)])[:10], round(float(b),2)) for a,b in zip(tk5[i,pos], tl5[i,pos])])
```