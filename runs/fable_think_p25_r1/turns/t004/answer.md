```python
# Pick a diagnostic set: 128 problems, roughly one per database, seeded; save split lists for later use
random.seed(0)
by_db = collections.defaultdict(list)
for p in probs: by_db[p['db']].append(p)
db_list = sorted(by_db)
random.shuffle(db_list)
diag = []
for db in db_list[:128]:
    diag.append(random.choice(by_db[db])['id'])
# a second disjoint set for later confirmation (different problems, mixed dbs)
used = set(diag)
pool = [p['id'] for p in probs if p['id'] not in used]
random.shuffle(pool)
confirm_pool = pool[:2000]
json.dump({"diag": diag, "confirm_pool": confirm_pool}, open(f"{WORK}/splits.json","w"))
print(diag[:10], len(diag))
pid = {p['id']: p for p in probs}
print(sum(lens[pid[i]['db']] for i in diag)/128)
```