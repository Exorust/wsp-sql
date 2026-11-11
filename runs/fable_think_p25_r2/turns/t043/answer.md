```python
# Hypothesis: build the loop measurement texts via token offsets; pick 14 shortest; plus 30 gold texts (non-thinking format) with short prompts
loopset_sorted=sorted(loopset,key=lambda d:d['end'])[:14]
loop_texts=[]
for d in loopset_sorted:
    ft=full_text(d['pid'],byid[d['pid']]['text'])
    enc=tok.encode(ft)
    off=enc.offsets[d['end']-1][1]
    t=ft[:off]
    ids=tok.encode(t).ids
    d['n']=len(ids); loop_texts.append(t)
print([ (d['pid'],d['n'],d['start'],d['P']) for d in loopset_sorted])
gen_ids=set(byid)
cands=[]
for pid,o in prac.items():
    if pid in gen_ids: continue
    pl=len(tok.encode(full_text(pid,'')).ids)
    if pl<180: cands.append((pl,pid))
cands.sort()
import random; random.seed(0)
gold_pids=[p for _,p in random.sample(cands[:400],30)]
gold_texts=[]
for pid in gold_pids:
    g=prac[pid]['gold'].strip()
    gold_texts.append("<|im_start|>user\n"+user_msg(pid)+"<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"+BT+"sql\n"+g+"\n"+BT+"<|im_end|>")
gl=[len(tok.encode(t).ids) for t in gold_texts]
print(len(cands), sum(d['n'] for d in loopset_sorted), sum(gl))
meta=dict(loop=loopset_sorted, gold=gold_pids)
json.dump(meta,open(W+'/tf_set_meta.json','w'))
req3={"type":"teacher_forced","model":"original","texts":loop_texts+gold_texts,"return":{"token_logprobs":True,"topk":5}}
s3=json.dumps(req3).replace(chr(96),'\\u0060'); open(W+'/tf3_req.json','w').write(s3); print(len(s3))
```