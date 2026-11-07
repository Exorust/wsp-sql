```python
# Compute the unembedding direction for </think> and its overlaps with the competing first-thinking tokens; design w
u = E[TT]*normw
comp = {t: tok.encode(t).ids[0] for t in ["Thinking","The","Okay","Let","Here","\n","\n\n","<think>"]}
print("||E[TT]||", float(E[TT].norm()), "||u||", float(u.norm()), "normw mean/max", float(normw.mean()), float(normw.max()))
for t,i in comp.items():
    ui = E[i]*normw
    print(repr(t), i, "cos(u,ui)", round(float((u@ui)/(u.norm()*ui.norm())),3), "||ui||", round(float(ui.norm()),2))
# residual rms at pos per layer
for L in [16,20,22,23]:
    hh=np.stack([H[L][i,pos_think[i]].astype(np.float32) for i in range(6)]); print(L, "rms", np.sqrt((hh**2).mean(1)).round(3), "max|h|", np.abs(hh).max(1).round(2))
```