```python
# Build edit v1: zero L23 digit-suppressor columns, halve L22n796, double L22n817/L23n879/L23n935 (down_proj columns)
def apply_edit(spec):
    # spec: {layer: {neuron: factor}}
    for L,d in spec.items():
        name=f'model.language_model.layers.{L}.mlp.down_proj.weight'
        Wn=load_original(name).clone()
        for n,f in d.items(): Wn[:,n]*=f
        save_edit(name,Wn)
v1={23:{580:0.,598:0.,564:0.,557:0.,485:0.,669:0.,639:0., 879:2.,935:2.}, 22:{796:0.5, 817:2.}}
apply_edit(v1); print(edited())
# prepare paired TF request: same 40 texts as pass 4, edited model
req8={'type':'teacher_forced','model':'edited','texts':r4['texts'],'return':{'token_logprobs':True,'topk':20}}
s=json.dumps(req8); print(len(s)); open(W+'/req8.json','w').write(s)
with open(W+'/notes.md','a') as f:
    f.write("""
## Key finding (pass 7 analysis)
- Section-advance decision after '\\n\\n' (indent '   ' vs next section digit) has margins 0.4-2.5 nats in loop texts.
- Final-layer MLP (L23) has DIGIT-SUPPRESSOR neurons that fire when a digit is about to be predicted and demote exactly that digit by ~3 nats:
  n580('3'), n598('5'), n564('4'), n557('1'), n485('2'), n669('6'), n639('7'). They tip the balance to indentation -> model keeps adding bullets.
- Bullet-end decision ('\\n' vs '\\n\\n'): soft points (margin<3) ~25%; neurons L22n817, L23n879, L23n935 push toward '\\n\\n' (fire at '.', '`', ')').
- L22n796: generic indent promoter active at newlines (+2..3.6 nats toward indent at '\\n\\n').
## Edit v1 (saved): L23 zero cols {580,598,564,557,485,669,639}; L23 x2 {879,935}; L22 x0.5 {796}; L22 x2 {817}. Testing with TF pass 8 on pass-4 texts.
""")
```