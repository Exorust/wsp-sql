```python
# MLP-neuron attribution for Thinking-vs-The and Thinking-vs-Okay at the first thinking token, layers 18..23
Wd={l:load_original(f'model.language_model.layers.{l}.mlp.down_proj.weight').numpy() for l in range(18,24)}
def neuron_attr(n,p,a,b,l):
    d=((E[a]-E[b])*(1+wn)).numpy(); r=np.sqrt((HF8[n][p]**2).mean())
    return M8[l][n,p].astype(np.float32)*(d@Wd[l])/r   # [3584]
for (a,b,name) in [(T_think,T_the,'Thinking-The'),(T_think,T_ok,'Thinking-Okay')]:
    print('==',name)
    for l in range(18,24):
        c0=neuron_attr(0,pfirst[0],a,b,l); c1=neuron_attr(1,pfirst[1],a,b,l); c=(c0+c1)/2
        top=np.argsort(-np.abs(c))[:5]
        print(f' L{l} total {c.sum():.2f} | top neurons', [(int(j), round(float(c[j]),2)) for j in top])
```