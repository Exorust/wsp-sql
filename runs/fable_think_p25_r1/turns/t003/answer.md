```python
# Load practice problems; look at distribution of dbs, schema sizes, gold query features
import random
probs = [json.loads(l) for l in open(f"{PRAC}/spider_train.jsonl")]
print(len(probs), probs[0])
dbs = collections.Counter(p['db'] for p in probs)
print(len(dbs), dbs.most_common(5))
schemas = {db: open(f"{PRAC}/schemas/{db}.sql").read() for db in dbs}
lens = {db: len(tok.encode(s).ids) for db, s in schemas.items()}
print("schema token lengths: min/median/max", min(lens.values()), np.median(list(lens.values())), max(lens.values()))
# write initial notes
open(f"{WORK}/notes.md","w").write("# Notes\n\n## State\n- 0/25 forward passes used.\n\n## Findings\n\n## Edits tried\n\n")
print(schemas[probs[0]['db']][:600])
```