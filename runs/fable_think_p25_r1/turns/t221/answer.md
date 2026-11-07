```python
# Build pass-13 TF request: model's own correct multi-line answers (legit line starts) + loop answers truncated (repetition line starts)
rows11=rows
print(repr(rows12[0]['text'][:30]))
def gen_text(r, max_chars=None):
    t=r['text']
    if max_chars: t=t[:max_chars]
    return "<|im_start|>user\n"+prompt_of(r['id'])+"<|im_end|>\n<|im_start|>assistant\n<think>\n"+t
allr={r['id']:r for r in rows11+rows12}
corr=[r for r in allr.values() if r['cls']=='correct' and str(r['cut'])!='True' and r['text'].count('\n')>=4]
corr.sort(key=lambda r: lens.get(r['id'], len(tok.encode(prompt_of(r['id'])).ids)))
print('multi-line correct candidates', len(corr), [ (r['id'], lens.get(r['id'])) for r in corr[:16]])
loops=[r for r in allr.values() if str(r['cut'])=='True']
def truncate_loop(t, reps=4):
    # find first exact-repeated line; cut after `reps` further lines
    lines=t.split('\n'); seen={}; cut=None
    for i,l in enumerate(lines):
        key=l.strip()
        if key and key in seen and i>seen[key]+0:
            cut=i; break
        seen.setdefault(key,i)
    if cut is None: return t[:1500]
    return '\n'.join(lines[:cut+reps])+'\n'
for r in loops:
    tt=truncate_loop(r['text']); print(r['id'], 'prompt toks', lens.get(r['id']) or len(tok.encode(prompt_of(r['id'])).ids), 'gen toks', len(tok.encode(tt).ids), '|', tt[-90:].replace('\n','|'))
```