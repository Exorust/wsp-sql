```python
# Verify transcription fidelity (lengths) and locate decision positions in gold SQL: after SELECT, after FROM table (+alias), end of query
d12=json.load(open(f'{W}/fwd_12.done.json'))
print('lengths match:', d12['lengths']==toks, sum(a!=b for a,b in zip(d12['lengths'],toks)))
lp12=np.load(f'{W}/fwd_12/token_logprobs.npy'); tk12=np.load(f'{W}/fwd_12/topk_ids.npy'); tkl12=np.load(f'{W}/fwd_12/topk_logprobs.npy')
print(lp12.shape, tk12.shape)
# tokenization of each text; find the SQL region (after '</think>\n\n```sql\n')
sql_start_marker=enc("</think>\n\n"+BT+"sql\n")
print('marker ids',sql_start_marker)
T12=[enc(t) for t in textsC]
def find_sub(ids,sub):
    for i in range(len(ids)-len(sub)+1):
        if ids[i:i+len(sub)]==sub: return i
    return -1
starts=[find_sub(ids,sql_start_marker)+len(sql_start_marker) for ids in T12]
print(starts[:10])
# decode SQL token-by-token for text 5 to see token boundaries
i=5; ids=T12[i]; print([tok.decode([t]) for t in ids[starts[i]:]])
```