```python
# How far does the model get before looping? Section headings reached per text in gen_1 and gen_7
import re
def sections(t):
    return re.findall(r'\n(\d+)\.\s+\*\*([^*]{1,40})\*\*', t)
rows7=[json.loads(l) for l in open(os.path.join(W,'gen_7.jsonl'))]
for name,rr in [('gen_1',rows),('gen_7',rows7)]:
    maxsec=collections.Counter(); heads=collections.Counter(); hasSel=0
    for r in rr:
        s=sections(r['text']); 
        if s: maxsec[max(int(a) for a,b in s)]+=1
        else: maxsec[0]+=1
        for a,b in s[:6]: heads[(a,b.strip())]+=1
        hasSel+= ('SELECT' in r['text'])
    print(name, 'max section reached:', sorted(maxsec.items()), 'hasSELECT', hasSel)
    print(heads.most_common(14))
```