```python
# Save TF request (edited model, 32 plain gold texts) and try referencing it by file in the forward block (free if rejected)
req={"type":"teacher_forced","model":"edited","texts":T[:32],"return":{"token_logprobs":True,"topk":10}}
json.dump(req,open(W+'/tf14_req.json','w')); print(os.path.getsize(W+'/tf14_req.json'))
```