```python
# Load fwd_13; locate SQL-region line-start decision positions ('\n' token inside the sql block) and the model's lp for next token vs alternatives (``` / AND / JOIN / OR)
D=f'{W}/fwd_13'; m13=json.load(open(f'{D}/meta.json'))
lp13=np.load(f'{D}/token_logprobs.npy'); tk_ids=np.load(f'{D}/topk_ids.npy'); tk_lp=np.load(f'{D}/topk_logprobs.npy')
print(lp13.shape, tk_ids.shape)
FENCE_ID=tok.encode('\n'+FENCE).ids; print('fence tokens', FENCE_ID, [tok.decode([i]) for i in FENCE_ID])
AND_ID=tok.encode('\nAND').ids; print('AND tokens', AND_ID, [tok.decode([i]) for i in AND_ID])
enc13=[tok.encode(t).ids for t in texts13]
for k in range(3): print(k, len(enc13[k]), m13['lengths'][k])
# decision positions: token p is '\n' (198) after the sql fence line, next token = line start
def sql_region(ids):
    # start = index after '```sql\n' ; return (start, end)
    s=None
    for i in range(len(ids)-3):
        if tok.decode(ids[i:i+3]).endswith('sql\n') and FENCE in tok.decode(ids[i:i+3]): s=i+3
    return s
starts=[sql_region(ids) for ids in enc13]; print(starts[:8])
```