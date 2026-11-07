```python
# Fix truncation of text a (search after </think>)
t_a=gen_text(allr['sp2951'])
j=t_a.find('</think>'); k1=t_a.find(FENCE+'sql',j); k2=t_a.find(FENCE,k1+6); t_a=t_a[:k2+3]+"<|im_end|>\n"
print(repr(t_a[-330:]))
req14={'type':'teacher_forced','model':'edited','texts':[t_a,t_b],'return':{'token_logprobs':True,'topk':10,'attn_layers':[3,7,11,15,19,23],'mlp_act':[20,21,22,23]}}
s14=json.dumps(req14).replace(FENCE,'\\u0060\\u0060\\u0060'); open(f'{W}/req14.json','w').write(s14)
print(len(s14), len(tok.encode(t_a).ids)); i0=s14.find('Question: What are the title'); print(s14[i0-50:i0+900])
```