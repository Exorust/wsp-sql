```python
# Hypothesis: late-layer neurons exist that fire selectively when the current line repeats an earlier line (repetition detectors). Test on fwd_7 (thinking loops).
m7=json.load(open(f'{W}/fwd_7/meta.json')); items7=json.load(open(f'{W}/req7_items.json')); req7=json.load(open(f'{W}/req7.json'))
print(m7['files']); print(type(items7), (list(items7.keys()) if isinstance(items7,dict) else items7[:3]))
texts7=req7['texts']; print(len(texts7), m7['lengths'])
NL=tok.encode('\n').ids; print('newline ids', NL, tok.encode('*   The').ids)
# tokenize and find, for each '\n'-token position, whether the following line already appeared earlier
def line_repeat_flags(text):
    ids=tok.encode(text).ids
    toks=[tok.decode([i]) for i in ids]
    flags=[]  # (pos_of_newline_token, is_repeat, line_text)
    seen=set(); cur=[]; start=None
    for p,t in enumerate(toks):
        if '\n' in t:
            line=''.join(cur).strip()
            if start is not None and line: flags.append((start,line in seen,line))
            seen.add(line); cur=[]; start=p
        else: cur.append(t)
    return ids,flags
ids0,fl0=line_repeat_flags(texts7[0]); print(len(ids0), len(fl0), sum(f[1] for f in fl0)); print([ (p,r,l[:50]) for p,r,l in fl0[:12]])
```