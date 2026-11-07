```python
# Hypothesis: steer the first thinking token to 'Okay' (Qwen-native free-form thinking) instead of '</think>' to test whether non-template thinking avoids loops; build the alternative edit (not yet saved).
gN=load('model.language_model.norm.weight'); E=load('model.language_model.embed_tokens.weight')
okay_id=tok.encode('Okay').ids; print(okay_id, tok.decode(okay_id))
def udir(tid):
    v=gN*E[tid]; return v/v.norm(), float(v.norm())
u_think,n_think=udir(END[0]); u_okay,n_okay=udir(okay_id[0]); print('norms',n_think,n_okay, 'cos',float(u_think@u_okay))
alphas={17:(537,0.20),18:(628,0.20),19:(2424,0.25),20:(1235,0.15)}
# verify current edit = original + alpha*u_think on those columns
for L,(n,a) in alphas.items():
    Wd=load('model.language_model.layers.%d.mlp.down_proj.weight'%L); W0=load_original('model.language_model.layers.%d.mlp.down_proj.weight'%L)
    d=Wd[:,n]-W0[:,n]; print(L,n,'delta norm',round(float(d.norm()),3),'cos with u_think',round(float(d@u_think/d.norm()),3),'col norm',round(float(W0[:,n].norm()),3))
```