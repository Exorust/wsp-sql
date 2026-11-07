```python
# Build the 2 chats for the attention pass (avoid literal triple backticks in code)
BT = chr(96)*3
def user_msg(p):
    return "Database schema (SQLite):\n" + schemas[p['db']] + "\n\nQuestion: " + p['question'] + "\n\nWrite one SQLite query that answers the question. Reply with the query in a " + BT + "sql code block."
gen_by_id={g['id']:g for g in gens}
def chat_for(gid, total=2048, margin=40):
    p=pid[gid]; u=user_msg(p); t=gen_by_id[gid]['text']
    nu=len(tok.encode(u).ids)
    ids=tok.encode(t).ids[: total-nu-margin]
    return [{"role":"user","content":u},{"role":"assistant","content":tok.decode(ids)}], nu, len(ids)
chats_attn=[]
for gid in ["sp5689","sp4584"]:
    c,nu,na=chat_for(gid); chats_attn.append(c); print(gid, nu, na)
json.dump(chats_attn, open(f"{WORK}/chats_attn.json","w"))
print(json.dumps(chats_attn)[:200])
```