```python
# Trim to 10 loop texts + 25 gold texts and print the request JSON in chunks
loopset_sorted=loopset_sorted[:10]; loop_texts=loop_texts[:10]; gold_pids=gold_pids[:25]; gold_texts=gold_texts[:25]
meta=dict(loop=loopset_sorted, gold=gold_pids); json.dump(meta,open(W+'/tf_set_meta.json','w'))
req3={"type":"teacher_forced","model":"original","texts":loop_texts+gold_texts,"return":{"token_logprobs":True,"topk":5}}
s3=json.dumps(req3).replace(chr(96),'\\u0060'); open(W+'/tf3_req.json','w').write(s3); print(len(s3))
print(s3[:9800])
```