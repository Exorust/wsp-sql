```python
# req14: TF edited, 2 texts (sp2951, sp5069) with attention at full-attention layers + topk
t_a=gen_text(allr['sp2951'])+"<|im_end|>\n"; t_b=gen_text(allr['sp5069'])+"<|im_end|>\n"
# truncate text a to the end of the first sql block
ia=t_a.find(FENCE, t_a.find(FENCE+'sql')+6); t_a=t_a[:ia+3]+"<|im_end|>\n"
print(repr(t_a[-350:])); print(repr(t_b[-250:]))
req14={'type':'teacher_forced','model':'edited','texts':[t_a,t_b],'return':{'token_logprobs':True,'topk':10,'attn_layers':[3,7,11,15,19,23],'mlp_act':[20,21,22,23]}}
s14=json.dumps(req14).replace(FENCE,'\\u0060\\u0060\\u0060'); open(f'{W}/req14.json','w').write(s14)
print(len(s14), len(tok.encode(t_a).ids), len(tok.encode(t_b).ids))
print(s14[:9800])
```