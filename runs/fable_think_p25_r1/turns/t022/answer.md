```python
# Rebuild request JSON with backticks escaped (\u0060) so forward blocks don't break
def safe_json(obj):
    return json.dumps(obj).replace(chr(96), "\\u0060")
req = {"type": "teacher_forced", "model": "original", "enable_thinking": True, "chats": chats_attn,
       "return": {"token_logprobs": True, "topk": 20, "hidden_states": list(range(25)), "mlp_act": list(range(24)), "attn_layers": [3,7,11,15,19,23]}}
sreq=safe_json(req)
assert json.loads(sreq)==req and BT not in sreq
open(f"{WORK}/req2.json","w").write(sreq)
print(len(sreq)); print(sreq[:9500])
```