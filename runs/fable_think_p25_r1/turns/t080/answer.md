```python
# Save a helper to write the request with a given model field; update notes
def req_json(model):
    r = dict(req4); r['model'] = model
    return json.dumps(r).replace("`"*3, "\\u0060\\u0060\\u0060")
open(W+"/req4_edited.json","w").write(req_json("edited"))
with open(W+"/notes.md","a") as f:
    f.write("""
- fwd_4 (pass 4, original): 16 loop texts (setA shortest) + 24 gold texts (setB shortest). Loop decision points (n=79 bullet-starts, 75 bullet-ends in loop region):
  copied token lp mean -0.46 (start) / -0.22 (end); best alternative ('Wait' at starts, '\\n\\n' at ends) lp mean -2.5/-2.3; median margin 1.6/1.9 nats.
  fwd_2 attention: L15h7 schema-section attends 0.44 prompt/0.53 own text, in loop 0.42 induction; L11h1 0.70 prompt / 0.20 induction. Induction heads also serve schema copying.
- Probe B (pass 5 planned): zero o_proj columns of L15h7, L11h1, L23h5, L19h5.
- Forward JSON must escape triple backticks as \\u0060\\u0060\\u0060 (else the block ends early). req4_edited.json holds the probe request.
""")
print("ok")
```