```python
# Inspect gen_7: how do the loops look with L23h5 zeroed? Compare the loop pattern to gen_1 for a few problems
g7=[json.loads(l) for l in open(f'{W}/gen_7.jsonl')]
def loop_start(t):
    # crude: first position where a 60-char chunk repeats later within 2000 chars
    for a in range(0,len(t)-200,20):
        ch=t[a:a+60]
        if t.find(ch,a+60,a+2500)>0: return a
    return -1
ls1=[loop_start(r['text']) for r in g1]; ls7=[loop_start(r['text']) for r in g7]
print('loop start chars median orig', np.median(ls1), 'edited', np.median(ls7))
print('n sections (double newline followed by digit) median orig', np.median([len(re.findall(r'\n\n\d+\.',r['text'])) for r in g1]), 'edited', np.median([len(re.findall(r'\n\n\d+\.',r['text'])) for r in g7]))
print('contains SELECT: orig', sum('SELECT' in r['text'] for r in g1), 'edited', sum('SELECT' in r['text'] for r in g7))
for r in g7[1:4]:
    t=r['text']; a=max(0,ls7[g7.index(r)]-200)
    print('----', r['id'], 'loop@',ls7[g7.index(r)]); print(t[a:a+900].replace('\n','\\n'))
```