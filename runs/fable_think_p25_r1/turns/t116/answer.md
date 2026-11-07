```python
# At the start of thinking: what does the model predict after "<think>\n"? lp of 'Thinking' vs '</think>' vs '\n'
think_id = tok.encode("<think>").ids[0]; print(think_id)
for i in range(6):
    ids_i=ids7[i]; pt = ids_i.index(think_id); 
    # position pt is <think>, pt+1 is '\n', pt+2 is 'Thinking'
    print(info[i][1], [tokstr(x) for x in ids_i[pt:pt+3]], "pred at pt+1 (after <think>):", [(tokstr(ti7[i,pt,k]), round(float(tl7[i,pt,k]),1)) for k in range(4)],
          "| pred at pt+2 (after <think>\\n):", [(tokstr(ti7[i,pt+1,k]), round(float(tl7[i,pt+1,k]),1)) for k in range(5)], "lp(</think>)=", lp_of(i,pt+2,TT))
```