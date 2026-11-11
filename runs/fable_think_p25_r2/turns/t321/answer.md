```python
# Analyze fwd_21: in-context gold-lp gains of INSTR2/3/4 vs base & INSTR1 (same 12 problems), and L16 directions vs v16
d21=os.path.join(W,'fwd_21'); lp21=np.load(os.path.join(d21,'token_logprobs.npy')); h21=np.load(os.path.join(d21,'hidden_L16.npy'),mmap_mode='r')
plan=json.load(open(os.path.join(W,'tf21_plan.json'))); sel=plan['sel']
def sqlpos(t,lp_row):
    pre=t.index(FENCE)+len(FENCE); return len(tok.encode(t[:pre]).ids), int(np.sum(~np.isnan(lp_row)))+1
def build(i,instr): 
    t=T[i]; k=t.index('Write one SQLite query'); return t[:k]+instr+'\n'+t[k:]
INS={'I2':plan['INSTR2'],'I3':plan['INSTR3'],'I4':plan['INSTR4']}
base=np.array([np.nanmean(lp13full[i,slice(*sqlpos(T[i],lp13full[i]))]) for i in sel])
i1=np.array([np.nanmean(lp13full[i+32,slice(*sqlpos(T[i+32],lp13full[i+32]))]) for i in sel])
print('base',base.mean().round(4),'INSTR1 gain',(i1-base).mean().round(4),'se',((i1-base).std()/np.sqrt(12)).round(4))
# base hidden dir
hb=[np.asarray(h[i,slice(*sqlpos(T[i],lp13full[i]))]).astype(np.float32).mean(0) for i in sel]
dirs={}
for v,(name,instr) in enumerate(INS.items()):
    g=[];hv=[]
    for j,i in enumerate(sel):
        r=v*12+j; t=build(i,instr); a,b=sqlpos(t,lp21[r]); g.append(np.nanmean(lp21[r,a:b])); hv.append(np.asarray(h21[r,a:b]).astype(np.float32).mean(0))
    g=np.array(g); dv=np.mean(hv,0)-np.mean(hb,0); dirs[name]=dv
    print(name,'gain vs base',(g-base).mean().round(4),'se',((g-base).std()/np.sqrt(12)).round(4),'| dir norm',np.linalg.norm(dv).round(3),'cos v16',(np.dot(dv,v16)/np.linalg.norm(dv)/np.linalg.norm(v16)).round(3))
np.save(os.path.join(W,'dirs21.npy'),np.stack([dirs['I2'],dirs['I3'],dirs['I4']]))
```