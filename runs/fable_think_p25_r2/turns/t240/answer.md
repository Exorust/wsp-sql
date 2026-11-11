```python
# Select 32 short problems (fresh), build 96 texts (V0,V1,V2), write request JSON with backticks escaped; print total size
random.seed(11)
cands=[pid for pid in prob if pid not in used]; random.shuffle(cands)
pool=[]; perdb=collections.Counter(); nj=0
for pid in cands:
    d=prob[pid]
    if perdb[d['db']]>=1: continue
    n=len(tok.encode(full_text(pid)).ids)
    if n>255: continue
    isj='JOIN' in d['gold'].upper()
    if isj and nj>=12: continue
    pool.append(pid); perdb[d['db']]+=1; nj+=isj
    if len(pool)>=32: break
print(len(pool), 'gold JOIN', nj, 'dbs', len(perdb))
texts13=[full_text(p) for p in pool]+[full_text(p,INSTR1) for p in pool]+[full_text(p,INSTR2) for p in pool]
lens=[len(tok.encode(t).ids) for t in texts13]; print('total tokens', sum(lens), 'max', max(lens))
json.dump({'pool':pool,'INSTR1':INSTR1,'INSTR2':INSTR2}, open(os.path.join(W,'tf13_meta.json'),'w'))
req13={"type":"teacher_forced","model":"edited","texts":texts13,"return":{"token_logprobs":True,"topk":10,"hidden_states":[10,12,14,16,18]}}
js=json.dumps(req13, ensure_ascii=True).replace(chr(96),'\\u0060')
open(os.path.join(W,'tf13_req.json'),'w').write(js)
print(len(js), 'chars; chunks of 9500:', (len(js)+9499)//9500)
```