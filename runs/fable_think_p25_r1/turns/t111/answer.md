```python
# Two-step exit decision in the success text: after sentence-ending '.', lp('\n') vs lp('\n\n'); then lp(</think>) after the newline
ids=ids7[0]
print("tokens after '.' in thinking:")
for p in range(1,pexit+1):
    if ids[p-1]==dot_id and ids[p] in (NL,NL2):
        ctx=tok.decode(ids[p-8:p]).replace("\n","⏎")
        a=lp_of(0,p,NL); b=lp_of(0,p,NL2); c=lp_of(0,p+1,TT)
        print(f"{p:5d} {ctx[-45:]:>45s} | next={tokstr(ids[p])!r:8} lp(nl)={a} lp(nl2)={b} | lp(</think>) after={c}")
```