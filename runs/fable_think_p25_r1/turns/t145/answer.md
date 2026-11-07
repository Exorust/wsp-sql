```python
# Find the digit-suppressor family in L23 (and L22): neurons whose output strongly demotes one specific digit token
dig=[tok.encode(str(k)).ids[0] for k in range(10)]
ED=torch.stack([E[d] for d in dig])*nw  # [10,1024]
# also tokens like '10','11'? check tokenization of '10'
print('10 ->',tok.encode('10').ids, '11 ->',tok.encode('11').ids)
for L in [22,23]:
    S=(ED@Wd[L]).numpy()   # [10,3584] effect of unit activation on digit logits (before rms scaling)
    # typical activation sign/magnitude at '\n\n' positions from data
    acts=np.concatenate([M[L][i,[j for j,x in enumerate(enc[i]) if x==271]] for i in range(6)],0)  # [npos,3584]
    amin=acts.min(0); amax=acts.max(0)
    # effective digit effect = S * extreme act (choose sign by larger magnitude)
    ext=np.where(np.abs(amin)>np.abs(amax),amin,amax)
    eff=S*ext[None,:]   # [10,3584]
    cand=[(n,int(np.argmin(eff[:,n])),round(float(eff[:,n].min()),2),round(float(ext[n]),1)) for n in range(3584) if eff[:,n].min()<-0.5]
    cand=sorted(cand,key=lambda t:t[2])
    print(f'L{L} digit-suppressing neurons at nlnl (digit, min effect*act, extreme act):', cand[:20])
```