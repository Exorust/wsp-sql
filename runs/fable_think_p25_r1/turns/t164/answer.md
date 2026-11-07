```python
# Inspect gen_9 edited vs original transcripts: where do they loop now?
import json
def readj(p):
    return [json.loads(l) for l in open(p)]
g9e = readj(f"{W}/gen_9_edited.jsonl"); g9o = readj(f"{W}/gen_9_original.jsonl")
print(g9e[0].keys())
for i in range(3):
    t = g9e[i]['text'] if 'text' in g9e[i] else g9e[i].get('output','')
    print("=== EDITED", g9e[i].get('id'), "len", len(t))
    print(t[:600].replace("\n","\\n"))
    print("...")
    print(t[-500:].replace("\n","\\n"))
```