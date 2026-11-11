```python
# Trim further: 6 loop texts + 16 gold texts (~28k chars) to keep pasting manageable
loopset_sorted=loopset_sorted[:6]; loop_texts=loop_texts[:6]; gold_pids=gold_pids[:16]; gold_texts=gold_texts[:16]
meta=dict(loop=loopset_sorted, gold=gold_pids); json.dump(meta,open(W+'/tf_set_meta.json','w'))
req3={"type":"teacher_forced","model":"original","texts":loop_texts+gold_texts,"return":{"token_logprobs":True,"topk":5}}
s3=json.dumps(req3).replace(chr(96),'\\u0060'); open(W+'/tf3_req.json','w').write(s3); print(len(s3))
print(s3[9800:19600])
```