```python
# Hypothesis: build compact measurement sets (short prompts) for teacher-forced comparisons; save metadata
notes="""# Notes (fable_think_p25_r2)
## Diagnosis (gen_1, 128 Spider-train problems, original model, 8192 max tokens)
- accuracy 4.7%, 100% cut at max tokens, 97.7% looping. Loops start at answer token ~90-600 (median ~chars 1800),
  periods 35-120 tokens: cyclic bullet lists of schema facts ('*   The `X` table has `Y`.', 'Does the `people` table contain `Name`? Yes.',
  '*Wait, is there a specific constraint on ...?*'). Never emits </think>. The 6 'correct' are flukes (first SELECT inside thinking).
- Core problem = thinking never terminates due to repetition loops.
## Attention analysis (fwd_2: 2 loop texts, attn patterns of layers 3,7,11,15,19,23)
- Induction heads (mass on earlier copies of NEXT token, loop vs pre-loop): L11h1 0.53-0.63 vs 0.27-0.32; L15h7 0.70-0.73 vs 0.41;
  L23h5 0.55-0.71 vs 0.35; L23h4 0.34-0.48 vs 0.28; L23h0 ~0.4 vs 0.2; L19h5/6/7 ~0.35 vs 0.2.
- Duplicate-token heads (mass on earlier copies of CURRENT token): L3h7 0.8, L3h4 0.4, L7h5/6/7 ~0.6, L11h3 0.36, L23h6 0.8.
- Loop logprobs: rep0 mean -0.13/-0.49, rep2 -0.02 (locks in). </think> at ~-12.
## Forward passes used: 2 (gen_1 diagnostic; fwd_2 attn)
"""
open(W+'/notes.md','w').write(notes)
# choose loop texts: short prompt, clear loop; truncate at loop_start + 3P (<=1000 tokens)
loopset=[]
for r in rows:
    pid=r['id']
    ids=tok.encode(full_text(pid,r['text'])).ids
    pl=len(tok.encode(full_text(pid,'')).ids)
    if pl>300: continue
    tail=ids[-1500:]; P=None
    for p in range(5,400):
        if np.mean(np.array(tail[p:])==np.array(tail[:-p]))>0.98: P=p; break
    if P is None or P<15: continue
    arr=np.array(ids); start=None
    for i in range(pl,len(ids)-60):
        seg=arr[i:i+P]
        if i+2*P<=len(arr) and np.array_equal(arr[i+P:i+2*P],seg): start=i; break
    if start is None: continue
    end=start+3*P+10
    if end>1000 or end>len(ids): continue
    loopset.append(dict(pid=pid,pl=pl,P=P,start=start,end=end))
print(len(loopset)); print(loopset[:5])
print('total tokens', sum(d['end'] for d in loopset))
```