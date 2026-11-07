```python
# Hypothesis: build a long-prompt robustness test (BIRD-like 3k-7k token schemas, with Hint lines) to check lp(</think>) at the first thinking position under the edit.
SCH='/Users/chandu/myproj/wsp-sql/practice/schemas/'
slen={f[:-4]:len(tok.encode(open(SCH+f).read()).ids) for f in os.listdir(SCH)}
top=sorted(slen.items(),key=lambda x:-x[1])[:12]; print(top)
prac=[json.loads(l) for l in open('/Users/chandu/myproj/wsp-sql/practice/spider_train.jsonl')]
bydb=collections.defaultdict(list)
for q in prac: bydb[q['db']].append(q)
used=set(gs['gen12'])|set(gs['genA'])|set(gs['genB'])|set(gs['genC'])|set(sp['diag']); print(len(used))
```