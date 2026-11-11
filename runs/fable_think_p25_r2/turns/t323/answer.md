```python
# Retry (fixed syntax): INSTR1 direction at L12/L14, constant neurons, save L14 steer edit
h12=np.load(os.path.join(W,'fwd_13','hidden_L12.npy'),mmap_mode='r'); h14=np.load(os.path.join(W,'fwd_13','hidden_L14.npy'),mmap_mode='r')
def instr_dir(hh):
    vb=[];va=[]
    for i in range(32):
        a0,a1=sqlpos(T[i],lp13full[i]); b0,b1=sqlpos(T[i+32],lp13full[i+32])
        vb.append(np.asarray(hh[i,a0:a1]).astype(np.float32).mean(0)); va.append(np.asarray(hh[i+32,b0:b1]).astype(np.float32).mean(0))
    return np.mean(va,0)-np.mean(vb,0)
v12=instr_dir(h12); v14=instr_dir(h14)
print('norms v12',np.linalg.norm(v12).round(3),'v14',np.linalg.norm(v14).round(3),'v16',np.linalg.norm(v16).round(3),'cos(v14,v16)',(np.dot(v14,v16)/np.linalg.norm(v14)/np.linalg.norm(v16)).round(3),'cos(v12,v16)',(np.dot(v12,v16)/np.linalg.norm(v12)/np.linalg.norm(v16)).round(3))
res={}
L0=int(mask[0].sum())
for L in [12,14]:
    m=np.load(os.path.join(W,'fwd_12',f'mlp_down_in_L{L}.npy'),mmap_mode='r'); A=np.asarray(m[:,:,:]).astype(np.float32)[mask]
    mu=A.mean(0); sd=A.std(0); z=np.abs(mu)/(sd+1e-6); top=np.argsort(-z)[:4]
    hres=np.load(os.path.join(W,'fwd_12',f'hidden_L{L}.npy'),mmap_mode='r'); rn=np.median(np.linalg.norm(np.asarray(hres[0,5:L0]).astype(np.float32),axis=1))
    print(f'L{L} resid norm {rn:.2f}; top const neurons',top.tolist(),'z',z[top].round(1).tolist(),'mean',mu[top].round(3).tolist(),'frac same sign',[float((np.sign(A[:,n])==np.sign(mu[n])).mean().round(3)) for n in top])
    res[L]=(int(top[0]),float(mu[top[0]]),rn)
Lsel=14; n_,a_,rn_=res[Lsel]; v=v14; colscale=5.6/abs(a_); col=np.sign(a_)*colscale*v
Wd=load_original(f'model.language_model.layers.{Lsel}.mlp.down_proj.weight').clone(); print('orig col norm',Wd[:,n_].norm().item()); Wd[:,n_]=torch.tensor(col); save_edit(f'model.language_model.layers.{Lsel}.mlp.down_proj.weight',Wd)
np.save(os.path.join(W,'v14.npy'),v14); np.save(os.path.join(W,'v12.npy'),v12)
print('saved L14 steer via neuron',n_,'act',round(a_,3),'col norm',np.linalg.norm(col).round(2),'expected steer norm',round(abs(a_)*np.linalg.norm(col),2),'edited:',edited())
```