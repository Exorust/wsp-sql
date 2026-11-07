```python
# Hypothesis: the 6 full-attention layers contain weight-identifiable "copy" heads (OV maps a token's embedding onto its own unembedding) that carry schema linking; first explore the environment, then score every head's OV/QK circuit from weights only.
import json, os, time, collections, numpy as np, torch
P='/Users/chandu/myproj/wsp-sql'; W=P+'/runs/smoke_fable/work'; M=P+'/models/Qwen3.5-0.8B'; LM='model.language_model.'
t0=time.time()
try:
    print(sorted(os.listdir(M)))
    cfg=json.load(open(M+'/config.json')); tc=cfg.get('text_config',cfg)
    print({k:(v if len(str(v))<120 else str(v)[:120]) for k,v in tc.items()})
except Exception as e: print('cfg err',repr(e))
print('n tensors',len(NAMES),'language_model',sum(n.startswith(LM) for n in NAMES))
for n in NAMES:
    if n.startswith(LM+'layers.3.') or n.startswith(LM+'layers.0.') or (n.startswith(LM) and '.layers.' not in n):
        print(' ',n.replace(LM,''),tuple(SHAPES[n]))
# practice data
probs=[json.loads(l) for l in open(P+'/practice/spider_train.jsonl')]
schemas={f[:-4]:open(P+'/practice/schemas/'+f).read() for f in os.listdir(P+'/practice/schemas') if f.endswith('.sql')}
slen={d:len(tok.encode(s).ids) for d,s in schemas.items()}
Ls=np.array([slen[p['db']] for p in probs])
print('n problems',len(probs),'dbs',len(schemas),'schema tokens pct 0/10/50/90/100',np.percentile(Ls,[0,10,50,90,100]))
print(probs[0]); print(probs[3500])
short=min(schemas,key=lambda d:slen[d]); print('shortest schema',short,slen[short]); print(schemas[short][:500])
enc=tok.encode("SELECT CAST(SUM(a) AS REAL) * 100 / COUNT(*) FROM t AS T1 WHERE CAST(CAST(x"); print([(i,tok.decode([i])) for i in enc.ids])
rng=np.random.default_rng(20261105)
idx=sorted(rng.choice(len(probs),248,replace=False).tolist())
sample=[probs[i]['id'] for i in idx]; json.dump(sample,open(W+'/sample_ids.json','w'))
print('SAMPLE',json.dumps(sample,separators=(',',':')))
# weight-only OV / QK analysis of the attention heads
def rms(x,w=None,eps=1e-6):
    y=x/(x.pow(2).mean(-1,keepdim=True)+eps).sqrt()
    return y if w is None else y*w
def one(L,key):
    c=[n for n in NAMES if n.startswith(f'{LM}layers.{L}.') and key in n]
    assert len(c)==1,(L,key,c); return c[0]
try:
    E=load(LM+'embed_tokens.weight'); gfin=load(LM+'norm.weight')
    cnt=collections.Counter()
    for s in schemas.values(): cnt.update(tok.encode(s).ids)
    for p in probs: cnt.update(tok.encode(' '+p['gold']).ids)
    ids=[i for i,_ in cnt.most_common()]
    print('unique tokens in schemas+gold',len(ids))
    S=ids if len(ids)<=6000 else np.random.default_rng(0).choice(ids,6000,replace=False).tolist()
    S=torch.tensor(S); ES=E[S].clone(); n=len(S); ar=torch.arange(n)
    def stats(Mx):
        d=Mx.diag(); z=((d.mean()-Mx.mean())/Mx.std()).item()
        top1=(Mx.argmax(1)==ar).float().mean().item()
        rank=(Mx>d[:,None]).float().mean(1).median().item()
        return z,top1,rank
    print('direct path E->U: z %.2f top1 %.3f medrank %.4f'%stats(rms(ES,gfin)@ES.T))
    res={}
    for L in [3,7,11,15,19,23]:
        try:
            Wq=load(one(L,'q_proj')); Wk=load(one(L,'k_proj')); Wv=load(one(L,'v_proj')); Wo=load(one(L,'o_proj'))
            gin=load(one(L,'input_layernorm'))
            try: qn=load(one(L,'q_norm')); kn=load(one(L,'k_norm'))
            except Exception as e: qn=kn=None; print('no q/k norm',repr(e)[:80])
            hd=256; nh=Wo.shape[1]//hd; nkv=Wv.shape[0]//hd; per=Wq.shape[0]//nh
            X=rms(ES,gin)
            print(f'layer {L}: nh {nh} nkv {nkv} q rows/head {per} |Wo| {Wo.norm():.1f} |Wv| {Wv.norm():.1f}')
            for h in range(nh):
                g=h//(nh//nkv)
                Vx=X@Wv[g*hd:(g+1)*hd].T; Oh=Wo[:,h*hd:(h+1)*hd]
                ov=stats(rms(Vx@Oh.T,gfin)@ES.T)
                k=X@Wk[g*hd:(g+1)*hd].T
                if kn is not None: k=rms(k,kn)
                q1=X@Wq[h*per:h*per+hd].T
                if qn is not None: q1=rms(q1,qn)
                qk1=stats(q1@k.T)
                if per>hd:
                    q2=X@Wq[h*per+hd:(h+1)*per].T
                    if qn is not None: q2=rms(q2,qn)
                    qk2=stats(q2@k.T); gn=Wq[h*per+hd:(h+1)*per].norm().item(); qnm=Wq[h*per:h*per+hd].norm().item()
                else: qk2=(float('nan'),)*3; gn=float('nan'); qnm=Wq[h*per:h*per+hd].norm().item()
                res[(L,h)]=dict(onorm=Oh.norm().item(),ov=ov,qk=qk1,qk2=qk2)
                print(f'  h{h} kv{g} |O|{Oh.norm():5.1f} |Q|{qnm:5.1f} |G|{gn:5.1f} OV z{ov[0]:+6.2f} top1 {ov[1]:.3f} rank {ov[2]:.3f} | QK(1st half) z{qk1[0]:+6.2f} top1 {qk1[1]:.3f} rank {qk1[2]:.3f} | QK(2nd half) z{qk2[0]:+6.2f} top1 {qk2[1]:.3f}')
        except Exception as e: print('layer',L,'err',repr(e)[:300])
except Exception as e: print('analysis err',repr(e)[:300])
print('elapsed %.0fs'%(time.time()-t0))
```