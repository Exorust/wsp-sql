```python
# Hypothesis: late full-attention heads (layers 19, 23) whose OV circuit writes the attended token's own identity into the logits are in-context "confirmation/copy" heads; boosting their output x1.5 should favour tokens present in the prompt (schema names) over invented ones. Prediction: fewer no_such_column/no_such_table, risk: more looping.
import re
for L in [15,19,23]:
    for h in range(8):
        r=res[(L,h)]; print(f'L{L} h{h} kv{h//4} |O|{r["onorm"]:.1f} OV z{r["ov"][0]:+.2f} top1 {r["ov"][1]:.3f} rank {r["ov"][2]:.3f} | QK z{r["qk"][0]:+.2f} top1 {r["qk"][1]:.3f}')
# what kind of tokens do the late heads copy? identifier-like (lowercase/underscore pieces) vs upper-case keyword-like
dec=[tok.decode([int(i)]) for i in S.tolist()]
is_ident=torch.tensor([bool(re.fullmatch(r'[ _]?[a-z_]{2,}',d)) for d in dec]); is_upper=torch.tensor([bool(re.fullmatch(r' ?[A-Z]{2,}',d)) for d in dec])
print('ident-like tokens',int(is_ident.sum()),'upper-case tokens',int(is_upper.sum()),'of',len(dec))
for L in [19,23]:
    Wv=load_original(one(L,'v_proj')); Wo=load_original(one(L,'o_proj')); X=rms(ES,load_original(one(L,'input_layernorm')))
    for h in range(8):
        g=h//4; Mx=rms((X@Wv[g*256:(g+1)*256].T)@Wo[:,h*256:(h+1)*256].T,gfin)@ES.T; d=Mx.diag(); mu=Mx.mean(); sd=Mx.std()
        print(f'  L{L} h{h} OV diag z: ident {((d[is_ident].mean()-mu)/sd).item():+.2f} upper {((d[is_upper].mean()-mu)/sd).item():+.2f} | top1 ident {(Mx.argmax(1)==ar)[is_ident].float().mean().item():.3f} upper {(Mx.argmax(1)==ar)[is_upper].float().mean().item():.3f}')
# candidate edit: boost the output (o_proj column block) of the clearest copy heads in layers 19 and 23
alpha=1.5; sel={}
for L in [19,23]:
    c=sorted([(res[(L,h)]['ov'][0],h) for h in range(8) if res[(L,h)]['ov'][0]>=3 and res[(L,h)]['ov'][1]>=0.3],reverse=True)[:3]
    sel[L]=[h for _,h in c]
print('selected copy heads',sel,'alpha',alpha)
for n in list(edited()): drop_edit(n)
for L,hs in sel.items():
    if not hs: continue
    name=one(L,'o_proj'); Wo=load_original(name).clone()
    for h in hs: Wo[:,h*256:(h+1)*256]*=alpha
    r=save_edit(name,Wo); print('saved',name,r,'rel change %.3f'%((Wo-load_original(name)).norm()/load_original(name).norm()).item())
print('edited:',edited())
notes=f"""# notes (smoke_fable)
Budget: 1 forward pass, 6 code runs. Plan: weight-only analysis -> candidate edit -> single paired 'both' generation (248 practice ids in sample_ids.json + 8 own BIRD-style prompts) -> keep only if paired gain clearly > SE, else drop all edits.
## Weight-only findings (run 1-2)
- Attn layers 3,7,11,15,19,23: q_proj rows per head = [256 query | 256 output gate]; query half shows token-matching QK structure, gate half none.
- OV circuit through tied unembedding (5422 schema/gold tokens): clear copy heads (token -> same token, top1 up to 0.98) and clear anti-copy heads (own token ranked last), e.g. L7h0 z-7.7 (QK same-token top1 0.98), L11h6 z-7.0; copy: L7h2 z+7.1, L11h7 z+6.5, L11h4 z+5.8, L3h0 z+5.6.
- late layers table: {json.dumps({f'L{L}h{h}':[round(res[(L,h)]['ov'][0],2),round(res[(L,h)]['ov'][1],3),round(res[(L,h)]['qk'][1],3)] for L in [15,19,23] for h in range(8)})} (OV z, OV top1, QK top1)
## Candidate edit 1 (UNVALIDATED until the paired pass)
- o_proj column blocks of heads {sel} scaled x{alpha}. Hypothesis: these heads confirm/copy in-context tokens; boost -> fewer invented columns; risk more loops.
"""
open(W+'/notes.md','w').write(notes)
```