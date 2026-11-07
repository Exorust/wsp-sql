```python
# Build Set A (loop decision probe) and Set B (gold SQL probe); save to files; try a file-reference request next
random.seed(1)
# Set A: looping gens, truncated at onset + 3 periods, rendered as generation context (variant B)
setA=[]
for gid,(o,p,hn,hb) in loopinfo.items():
    if not hn: continue
    ids=tok.encode(gen_by_id[gid]['text']).ids[:o+3*p]
    txt=render(user_msg(pid[gid]), tok.decode(ids), 'B')
    setA.append({"id":gid,"onset":o,"period":p,"text":txt})
print(len(setA), np.mean([len(tok.encode(x['text']).ids) for x in setA]))
# Set B: gold SQL in no-think form
poolB=[i for i in confirm_pool[1000:1300]]
setB=[]
for gid in poolB[:200]:
    p=pid[gid]
    txt=render(user_msg(p), BT+"sql\n"+p['gold']+"\n"+BT, 'A')
    setB.append({"id":gid,"text":txt})
print(len(setB), np.mean([len(tok.encode(x['text']).ids) for x in setB]))
json.dump(setA, open(f"{WORK}/setA.json","w")); json.dump(setB, open(f"{WORK}/setB.json","w"))
reqA={"type":"teacher_forced","model":"original","texts":[x['text'] for x in setA]+[x['text'] for x in setB],"return":{"token_logprobs":True,"topk":20}}
open(f"{WORK}/req3.json","w").write(json.dumps(reqA))
print(len(json.dumps(reqA)))
```