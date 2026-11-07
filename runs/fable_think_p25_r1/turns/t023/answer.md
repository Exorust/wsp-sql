```python
# Shorten the loop region to ~12 repetitions to keep the request small
def shorten(gid, nrep=12):
    p=pid[gid]; u=user_msg(p); t=gen_by_id[gid]['text']
    ids=tok.encode(t).ids
    o,per=find_loop(ids)
    ids=ids[:o+per*nrep]
    return [{"role":"user","content":u},{"role":"assistant","content":tok.decode(ids)}], len(tok.encode(u).ids), len(ids), o, per
chats_attn=[]
for gid in ["sp5689","sp4584"]:
    c,nu,na,o,per=shorten(gid, nrep=10); chats_attn.append(c); print(gid, nu, na, o, per)
req["chats"]=chats_attn
sreq=safe_json(req); assert json.loads(sreq)==req and BT not in sreq
print(len(sreq)); print(sreq)
```