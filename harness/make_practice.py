"""Build the practice set the editor may use: Spider train (7,000 questions, 146 databases). Never dev/Mini-Dev.
Writes practice/spider_train.jsonl (id, db, question, gold) and practice/schemas/<db>.sql (CREATE TABLE text)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from eval_sql import load_bench, schema_ddl, run_sql

out = os.path.join(os.path.dirname(__file__), "..", "practice")
os.makedirs(f"{out}/schemas", exist_ok=True)
items = load_bench("spider", "train")
kept, bad = 0, 0
with open(f"{out}/spider_train.jsonl", "w") as f:
    for it in items:
        if not os.path.exists(it["db_path"]):
            bad += 1; continue
        gold, err = run_sql(it["db_path"], it["gold"])
        if err:  # gold that does not run is useless as a label
            bad += 1; continue
        f.write(json.dumps(dict(id=f"sp{it['id']}", db=it["db"], question=it["question"], gold=it["gold"])) + "\n"); kept += 1
        p = f"{out}/schemas/{it['db']}.sql"
        if not os.path.exists(p):
            open(p, "w").write(schema_ddl(it["db_path"]))
print(f"kept {kept}, dropped {bad} (missing db or gold fails); schemas: {len(os.listdir(f'{out}/schemas'))}")
