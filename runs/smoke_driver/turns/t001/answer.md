```python
# Hypothesis: existing diagnostics or conspicuous weight anomalies may support a targeted candidate that can be tested with the single paired forward pass.
import os, json, pathlib, collections, math
import numpy as np
import torch

ROOT = pathlib.Path("/Users/chandu/myproj/wsp-sql")
WORK = ROOT / "runs/smoke_driver/work"
PRACTICE = ROOT / "practice"
for p in [
    pathlib.Path("/Users/chandu/.agents/skills/unslop/SKILL.md"),
    pathlib.Path("/Users/chandu/.agents/skills/anti-ai-slop-writing/SKILL.md"),
]:
    if p.exists():
        print("SKILL", str(p), p.read_text()[:12000])
print("WORK FILES", [(p.name, p.stat().st_size) for p in WORK.iterdir()] if WORK.exists() else [])
print("CURRENT EDITS", edited())
print("TENSORS", len(NAMES))
print("LAYER 23 SHAPES", [(n, SHAPES[n]) for n in NAMES if ".layers.23." in n])
print("MODEL CONFIG", (ROOT / "models/Qwen3.5-0.8B/config.json").read_text()[:6500])
problems = [json.loads(s) for s in (PRACTICE / "spider_train.jsonl").read_text().splitlines() if s.strip()]
print("PRACTICE", len(problems), "databases", len({p["db"] for p in problems}))
print("EXAMPLES", [{k:p[k] for k in ("id","db","question","gold")} for p in problems[:3]])
for p in sorted(WORK.glob("gen_*.jsonl")):
    print("EXISTING GENERATION FILE", p.name, p.stat().st_size)
for p in sorted(WORK.glob("*.md")):
    print("EXISTING NOTES", p.name, p.read_text()[:4000])
```
