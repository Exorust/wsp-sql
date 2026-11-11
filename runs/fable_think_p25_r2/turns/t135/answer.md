```python
# Look at request formats for fwd_3 (gold chats + loop texts) and the fwd_3 meta
print(open(os.path.join(W,'tf3_req.json')).read()[:1200])
m3=json.load(open(os.path.join(W,'fwd_3','meta.json'))); print({k:(v if not isinstance(v,list) else v[:5]) for k,v in m3.items()})
print(open(os.path.join(W,'edited_model','chat_template.jinja')).read()[-1500:])
```