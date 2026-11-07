```python
# Re-emit chat JSON with all backticks as \u0060 escapes so the forward block isn't broken by ``` sequences
def safe_json(obj):
    return json.dumps(obj).replace("`", "\\u0060")
req = {"type": "teacher_forced", "model": "original", "enable_thinking": True, "chats": chats_attn,
       "return": {"token_logprobs": True, "topk": 20, "hidden_states": list(range(25)), "mlp_act": list(range(24)), "attn_layers": [3,7,11,15,19,23]}}
s=safe_json(req)
print(len(s))
assert "```" not in s
# verify roundtrip
assert json.loads(s)==req
open(f"{WORK}/req2.json","w").write(s)
print(s[:9800])
```