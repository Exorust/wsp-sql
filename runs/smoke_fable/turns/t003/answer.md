```python
# Hypothesis: L23 h2 (QK same-token top1 0.905, OV ranks the source token's own logit LAST, z -5.0) is a final-layer copy-suppression head: it attends to positions carrying the token being predicted and pushes that token's logit down -> biases against tokens present in the prompt (schema names). Check the distance dependence of its same-token QK kernel under RoPE (self-only vs long-range) and the sign/size of its OV map, then knock it out as the candidate edit.
rp=tc.get('rope_parameters'); print(rp)
theta=float(rp.get('rope_theta',1e7)); prf=float(rp.get('partial_rotary_factor',1.0)); hd=256; rd=int(round(hd*prf)); nf=rd//2
th=theta**(-torch.arange(nf).float()*2/rd); print('rotary dims',rd,'freq pairs',nf)
ds=[0,1,2,4,16,64,256,1024]
perms=[torch.randperm(n,generator=torch.Generator().manual_seed(s)) for s in range(4)]
def kern(L,h):
    Wq=load_original(one(L,'q_proj')); Wk=load_original(one(L,'k_proj')); qn=load_original(one(L,'q_norm')); kn=load_original(one(L,'k_norm'))
    X=rms(ES,load_original(one(L,'input_layernorm'))); g=h//4
    q=rms(X@Wq[h*512:h*512+256].T,qn); k=rms(X@Wk[g*256:(g+1)*256].T,kn)
    def parts(q,k):
        u=(q[:,rd:]*k[:,rd:]).sum(1)
        a=q[:,:nf]*k[:,:nf]+q[:,nf:rd]*k[:,nf:rd]; b=q[:,:nf]*k[:,nf:rd]-q[:,nf:rd]*k[:,:nf]
        return u,a,b
    u,a,b=parts(q,k); offs=[parts(q,k[p]) for p in perms]
    uo=torch.cat([o[0] for o in offs]); ao=torch.cat([o[1] for o in offs]); bo=torch.cat([o[2] for o in offs])
    out={'U':((u.mean()-uo.mean())/16).item(),'sd':((uo+ao.sum(1)).std()/16).item(),'abs':(u.mean()/16).item()}
    for d in ds:
        c=torch.cos(d*th); s=torch.sin(d*th)
        out[d]=((((a@c).mean()-(ao@c).mean())/16).item(),(((b@s).mean()-(bo@s).mean())/16).item())
    return out
print('same-token attention-logit advantage over a random token (nats): U=unrotated dims; then total cos-part U+A(d) [sin-part B(d)] per distance d; sd=offdiag sd')
heads=[(3,4),(3,5),(3,7),(7,0),(7,2),(7,5),(7,6),(7,7),(11,3),(11,4),(11,6),(11,7),(15,1),(15,3),(15,5),(15,7),(19,4),(23,0),(23,2),(23,5),(23,6)]
K={}
for (L,h) in heads:
    o=kern(L,h); K[(L,h)]=o
    print(f'L{L}h{h} OVz{res[(L,h)]["ov"][0]:+5.1f} U{o["U"]:+5.2f} sd{o["sd"]:.2f} | '+' '.join(f'd{d}:{o["U"]+o[d][0]:+.2f}[{o[d][1]:+.2f}]' for d in ds))
print('norm weights first-64 vs rest: q_norm %.2f/%.2f k_norm %.2f/%.2f (L23)'%(load_original(one(23,'q_norm'))[:rd].abs().mean(),load_original(one(23,'q_norm'))[rd:].abs().mean(),load_original(one(23,'k_norm'))[:rd].abs().mean(),load_original(one(23,'k_norm'))[rd:].abs().mean()))
# OV map of every L23 head on token directions: cosine between its (final-norm-weighted) output and the source token's unembedding; mean output gate
for L in [23,15]:
    Wv=load_original(one(L,'v_proj')); Wo=load_original(one(L,'o_proj')); Wq=load_original(one(L,'q_proj')); X=rms(ES,load_original(one(L,'input_layernorm')))
    for h in range(8):
        g=h//4; out=(X@Wv[g*256:(g+1)*256].T)@Wo[:,h*256:(h+1)*256].T
        cs=torch.nn.functional.cosine_similarity(out*gfin,ES,dim=1)
        gate=torch.sigmoid(X@Wq[h*512+256:(h+1)*512].T)
        print(f'  L{L}h{h} cos(OV(tok),unembed(tok)) mean {cs.mean():+.3f} frac<0 {(cs<0).float().mean():.3f} | |OV out| {out.norm(dim=1).mean():.2f} | gate mean {gate.mean():.3f} (ident {gate[is_ident].mean():.3f} upper {gate[is_upper].mean():.3f})')
# candidate edit T1: knock out head L23 h2 (zero its o_proj column block)
for nme in list(edited()): drop_edit(nme)
name=one(23,'o_proj'); Wo=load_original(name).clone(); Wo[:,2*256:3*256]=0.0
print('save:',save_edit(name,Wo)); chk=load(name)
print('edited:',edited(),'| block norm now',chk[:,512:768].norm().item(),'| rel change of tensor %.3f'%((chk-load_original(name)).norm()/load_original(name).norm()).item())
open(W+'/notes.md','a').write("""
## Run 3: late layers have NO token-space copy heads (L19/L23 OV z<1 except L19h4 +2.4); copy heads sit in L7/L11/L15 (L15h1 z+4.9).
- L23h2: QK same-token top1 0.905, OV own-token rank LAST (z -5.0, ident -5.5, upper -5.4) -> final-layer copy-suppression head candidate. L23h6: QK top1 0.97, OV weakly negative (z -1.0).
## Candidate edit T1 (replaces candidate 1, which selected no heads): zero o_proj[:,512:768] of layer 23 (= head 2 knocked out).
- Prediction: fewer invented columns (no_such_column down), risk: more repetition/looping. To be tested in the single paired 'both' pass on sample_ids.json (248 ids) + 8 own BIRD-style prompts. KEEP ONLY IF paired gain clearly > SE; otherwise drop_edit everything.
""")
```