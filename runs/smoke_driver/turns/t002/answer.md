```python
# Hypothesis: a pre-existing diagnostic or isolated weight anomaly could justify a candidate without spending the only forward pass on exploration.
print("CURRENT EDITS", edited())
print("WORK FILES", [(p.name, p.stat().st_size) for p in WORK.iterdir()] if WORK.exists() else [])
print("TENSORS", len(NAMES))
print("LAYER 23 SHAPES", [(n, SHAPES[n]) for n in NAMES if ".layers.23." in n])
config_path = ROOT / "models/Qwen3.5-0.8B/config.json"
try:
    config = json.loads(config_path.read_text())
    print("TEXT CONFIG", config.get("text_config", config))
except Exception as e:
    print("CONFIG UNAVAILABLE", type(e).__name__, str(e)[:160])
problems = [json.loads(s) for s in (PRACTICE / "spider_train.jsonl").read_text().splitlines() if s.strip()]
print("PRACTICE", len(problems), "databases", len({p["db"] for p in problems}))
print("EXAMPLES", [{k:p[k] for k in ("id","db","question","gold")} for p in problems[:2]])
for p in sorted(WORK.glob("*.md")):
    print("EXISTING NOTES", p.name, p.read_text()[:3000])
for p in sorted(WORK.glob("gen_*.jsonl")):
    print("EXISTING GENERATIONS", p.name, p.stat().st_size)

# These are weight statistics, not a simulation of network computation.
weight_stats = []
for layer in range(24):
    name = f"model.language_model.layers.{layer}.mlp.down_proj.weight"
    w = load_original(name)
    norms = torch.linalg.vector_norm(w, dim=0)
    top = torch.topk(norms, 3)
    weight_stats.append({
        "layer": layer, "finite": bool(torch.isfinite(w).all()),
        "median_column_norm": round(float(norms.median()), 4),
        "p99_column_norm": round(float(torch.quantile(norms, 0.99)), 4),
        "top_neurons": top.indices.tolist(),
        "top_norms": [round(float(x), 4) for x in top.values],
        "max_to_median": round(float(norms.max()/norms.median()), 2),
    })
    del w
print("MLP DOWN-PROJECTION AUDIT")
for row in weight_stats:
    print(json.dumps(row))

# A seeded, database-stratified diagnostic sample; selection does not use answers.
rng = np.random.default_rng(20261104)
by_db = collections.defaultdict(list)
for p in problems:
    by_db[p["db"]].append(p)
queues = {}
for db, items in by_db.items():
    order = rng.permutation(len(items))
    queues[db] = [items[int(i)] for i in order]
selected = []
while len(selected) < 512:
    dbs = list(queues)
    rng.shuffle(dbs)
    for db in dbs:
        if queues[db]:
            selected.append(queues[db].pop())
            if len(selected) == 512:
                break
        else:
            del queues[db]
selected_ids = [p["id"] for p in selected]
print("DIAGNOSTIC_DATABASES", len({p["db"] for p in selected}))
print("DIAGNOSTIC_IDS", json.dumps(selected_ids))
```
