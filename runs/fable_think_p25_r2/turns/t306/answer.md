```python
# How were fwd_13 texts constructed (which halves have INSTR1/INSTR2)? And how was v16 computed (position set)?
req13=json.load(open(os.path.join(W,'tf13_req.json')))
T=req13['texts'] if 'texts' in req13 else req13['chats']; print(type(T[0]), len(T), list(req13.get('return',{}).keys()))
meta=json.load(open(os.path.join(W,'tf13_meta.json')))
for i in [0,31,32,63]:
    s=T[i] if isinstance(T[i],str) else T[i][0]['content']
    print(i,'INSTR1' in s or meta['INSTR1'][:30] in s, meta['INSTR2'][:30] in s, len(s))
# recompute candidate v16 from fwd_13 hidden_L16 over SQL-answer tokens to confirm definition
h=np.load(os.path.join(W,'fwd_13','hidden_L16.npy'), mmap_mode='r'); lp=np.load(os.path.join(W,'fwd_13','token_logprobs.npy'))
def sql_pos(t):
    pre=t.index(FENCE)+len(FENCE); npre=len(tok.encode(t[:pre]).ids); L=int(np.sum(~np.isnan(lp[T.index(t)])))+1; return npre,L
vb=[];va=[]
for i in range(32):
    a0,a1=sql_pos(T[i]); b0,b1=sql_pos(T[i+32])
    vb.append(np.asarray(h[i,a0:a1]).astype(np.float32).mean(0)); va.append(np.asarray(h[i+32,b0:b1]).astype(np.float32).mean(0))
vdiff=np.mean(va,0)-np.mean(vb,0)
print('recomputed diff norm',np.linalg.norm(vdiff).round(3),'cos with v16',(np.dot(vdiff,v16)/np.linalg.norm(vdiff)/np.linalg.norm(v16)).round(3))
```