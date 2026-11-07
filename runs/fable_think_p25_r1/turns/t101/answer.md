```python
# Build the pass-7 text set: success text, original loop texts (with 'Wait' bullets), edited loop texts, and constructed 'conclude+</think>+gold' texts
PRE = "<|im_start|>user\n"; MID = "<|im_end|>\n<|im_start|>assistant\n<think>\n"
def render(pid, ans): return PRE+user_msg(pid)+MID+ans
def trunc_tokens(s, n):
    ids=tok.encode(s).ids; return tok.decode(ids[:n]) if len(ids)>n else s
texts=[]; info=[]
# (1) success
r=done[0]; texts.append(render(r['id'], r['text'])); info.append(('success', r['id']))
# (2) original loop texts with "Wait" (choose ones whose loop unit contains 'Wait' or 'correct')
sel_o = [r for r in go if r['text'].count('Wait')>=5][:7]
for r in sel_o:
    full = render(r['id'], r['text']); texts.append(trunc_tokens(full, 1600)); info.append(('orig_loop', r['id']))
# (3) constructed: cut after a conclusion sentence then </think> + gold
concl = re.compile(r"(is correct\.|is the correct query\.|This should work\.|I think I have it\.|should be correct\.)\n")
nconst=0
for r in go:
    m = concl.search(r['text'])
    if m and nconst<4:
        cut = r['text'][:m.end()]
        if len(tok.encode(cut).ids) > 1300: continue
        ans = cut + "</think>\n\n" + FENCE+"sql\n"+prob[r['id']]['gold']+"\n"+FENCE
        texts.append(render(r['id'], ans)); info.append(('constructed', r['id'])); nconst+=1
# (4) edited loop texts
for r in ge[:3]:
    texts.append(trunc_tokens(render(r['id'], r['text']),1600)); info.append(('edited_loop', r['id']))
lens=[len(tok.encode(t).ids) for t in texts]
print(len(texts), lens, sum(len(t) for t in texts))
print(info)
json.dump({'texts':texts,'info':info}, open(W+"/req7_items.json","w"))
```