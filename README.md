# wsp-sql

Weight-space programming (an LLM edits a small model's weights directly, no gradients) applied to Qwen3.5-0.8B on
text-to-SQL. Replicates "Sparks of Weight-Space Programming" (Takehi, Teoh, Zhang, Khattab, MIT CSAIL, 2026-11-02)
with SQL instead of math. Plan and rationale: PLAN.md. Results: STATUS.md.

## Layout
- `eval_sql.py` : execution-accuracy evaluation of any model dir on BIRD Mini-Dev or Spider dev (mlx-lm, greedy by default); `--rep-penalty` is the decoding-only control.
- `harness/kernel.py` : persistent Python kernel over the weights (NAMES, load, save_edit...), sandboxed with sandbox-exec: no network, writes only in the run's work dir, reads only this project.
- `harness/forward.py` : forward-pass tool (graded generation incl. paired original-vs-edited; teacher-forced log-probs / hidden states / MLP acts / attention).
- `harness/driver.py` : run loop; one `codex exec` (gpt-6-astra, all Codex tools off, config in harness/codex_home) per turn; handoff every 40 turns; resumable via state.json.
- `harness/prompt.md` : the task prompt (the paper's first-turn prompt, SQL version).
- `harness/make_practice.py` : builds practice/ (Spider train, 6,997 questions, 140 schemas). Spider dev and BIRD Mini-Dev are never shown to the editor.
- `ref/` : the authors' released prompt, Codex config, sandbox sketch and exp8 README.
- `runs/p0_*` : Phase 0 (obstacle check). `runs/wsp_*` : editing sessions (turns/, work/, requests/, final_answer.md).

## Run
    .venv/bin/python eval_sql.py --model models/Qwen3.5-0.8B --bench bird --thinking 0 --max-tokens 1024 --out runs/x
    .venv/bin/python harness/driver.py --run runs/wsp_p25 --passes 25 --protocol nothink
