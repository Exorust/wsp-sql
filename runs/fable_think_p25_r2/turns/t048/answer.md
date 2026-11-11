```python
# Hypothesis: define baseline metrics on fwd_3 (loop regions and gold SQL) to compare later edits against
def analyze(fdir, verbose=True):
    lp=np.load(fdir+'/token_logprobs.npy'); tki=np.load(fdir+'/topk_ids.npy')
    out={}
    # loop set
    regs={'pre':[], 'rep0':[], 'rep1':[], 'rep2':[]}
    top1={'pre':[], 'rep1':[], 'rep2':[]}
    for i,d in enumerate(meta['loop']):
        ids=tok.encode(loop_texts[i]).ids; T=len(ids)
        pl,st,P=d['pl'],d['start'],d['P']
        bounds={'pre':(pl+1,st),'rep0':(st,st+P),'rep1':(st+P,st+2*P),'rep2':(st+2*P,T)}
        for k,(a,b) in bounds.items():
            regs[k].append(np.nanmean(lp[i,a:b]))
            if k in top1:
                pred=tki[i,a-1:b-1,0]; act=np.array(ids[a:b]); top1[k].append(np.mean(pred==act))
    for k in regs: out['loop_'+k]=float(np.mean(regs[k]))
    for k in top1: out['top1_'+k]=float(np.mean(top1[k]))
    # gold set
    g_lp=[]; g_top1=[]; g_min=[]
    for j,pid in enumerate(meta['gold']):
        i=len(meta['loop'])+j
        ids=tok.encode(gold_texts[j]).ids
        # find sql region: after the token sequence for "sql\n" following the think close; locate by decoding
        text=gold_texts[j]; s=text.rfind(BT+'sql\n')+len(BT+'sql\n'); e=text.rfind('\n'+BT)
        enc=tok.encode(text); offs=enc.offsets
        pos=[t for t,(a,b) in enumerate(offs) if a>=s and b<=e]
        a,b=pos[0],pos[-1]+1
        g_lp.append(np.nanmean(lp[i,a:b])); g_min.append(np.nanmin(lp[i,a:b]))
        pred=tki[i,a-1:b-1,0]; act=np.array(ids[a:b]); g_top1.append(np.mean(pred==act))
    out['gold_lp']=float(np.mean(g_lp)); out['gold_top1']=float(np.mean(g_top1)); out['gold_min']=float(np.mean(g_min))
    out['_gold_lp_each']=np.round(g_lp,2); out['_loop_rep2_each']=np.round(regs['rep2'],3); out['_loop_pre_each']=np.round(regs['pre'],3)
    if verbose:
        for k,v in out.items(): print(k, v if isinstance(v,np.ndarray) else round(v,4))
    return out
base=analyze(W+'/fwd_3')
```