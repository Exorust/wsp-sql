# Weight-space programming, but for SQL

An independent test of the claim in MIT CSAIL's *Sparks of Weight-Space Programming* (Takehi, Teoh, Zhang, Khattab, 2 November 2026): that a frontier language model, given a small model's weights and a budget of forward passes, can find why the small model misbehaves and fix it by editing the weights directly, with no training.

Same small model as the report, Qwen3.5-0.8B. A new task, text-to-SQL. A new editor, Claude Fable 5.1. The full trace of what the editor tried, the edit it submitted, held-out numbers, and controls.

- **Paper (draft):** [paper/main.pdf](paper/main.pdf)
- **Blog post:** [charoori.com/blog/weight-space-programming-sql](https://charoori.com/blog/weight-space-programming-sql)
- **Interactive explainer:** [wsp-sql.vercel.app](https://wsp-sql.vercel.app)

## The result in one paragraph

With thinking enabled, Qwen3.5-0.8B loops on 91% of SQL questions and gets 0.7% right. The editor made three attempts. Two were built from specific, measured mechanistic hypotheses about the loop (induction heads; digit-suppressing neurons in the last layer) and did nothing. The third found four neurons that fire only at the first thinking token and made them write the `</think>` direction: 4,083 weight entries. On 150 held-out BIRD Mini-Dev questions that edit cuts the loop rate from 90.7% to 26.0% and raises accuracy from 0.7% to 6.0%. Five random-location edits of the same size do nothing. Gradient descent restricted to the same 4,083 entries reaches the same behaviour. And the base model with thinking disabled through its chat template scores 7.3%. The edit is a bypass of the looping mode, not a repair of it.

| Condition (BIRD Mini-Dev, 150 q, greedy, 8,192 tokens) | Correct | Cut at limit | Looping |
|---|---|---|---|
| Base, thinking on | 0.7% | 98.7% | 90.7% |
| Base, thinking off via template | 7.3% | 12.0% | 11.3% |
| Report's math edit | 3.3% | 87.3% | 82.0% |
| Fable's edit (4,083 entries) | 6.0% | 27.3% | 26.0% |
| Random location, same size, 5 draws (50 q each) | 0 to 2% | 100% | 90 to 98% |
| Gradient descent on the same 4,083 entries | 4.7% | 30.7% | 29.3% |

## Reproduce the headline number

You need Python 3.11, an Apple-silicon Mac (the evaluation uses mlx-lm), and the public `Qwen/Qwen3.5-0.8B` checkpoint in `models/Qwen3.5-0.8B`.

```bash
uv venv .venv && uv pip install -r requirements.txt
python release/edit.py apply release/fable_r1_edit_c.npz models/Qwen3.5-0.8B out/edited_model
python eval_sql.py --model out/edited_model --bench bird --thinking 1 --max-tokens 8192 --batch 8 --n 150 --out runs/check
```

`release/fable_r1_edit_c.npz` is 19 KB and holds only the four changed columns; `release/edit.py apply` rebuilds the editor's checkpoint bit for bit. The evaluation takes about 20 minutes. Put BIRD Mini-Dev (the `minidev` release from the BIRD project) at `data/bird_minidev/minidev/MINIDEV/`; the Spider practice set the editor used is already in `practice/`.

## What is where

| Path | What it is |
|---|---|
| `runs/fable_think_p25_r1/` | The editing session. `turns/t001` to `t328`: every prompt and reply. `work/notes.md`: the editor's own notes. `final_answer.md`: its submission. |
| `release/` | The submitted edit as a small file, and the script to pack or apply an edit. |
| `paper/` | LaTeX source, figures (mermaid sources and rendered PDFs), compiled PDF, blog draft. |
| `site/` | The explainer website, plain HTML. |
| `harness/` | The re-implemented harness: `kernel.py` (sandboxed Python over the weights), `forward.py` (generation and teacher-forced passes), `driver.py` (the turn loop, `--editor fable` or `codex`), `prompt.md` (the task prompt). |
| `eval_sql.py` | Execution-accuracy evaluation on BIRD Mini-Dev or Spider. |
| `control_random.py` | Random-location control: same change vectors on random columns. |
| `baseline_sft.py` | Same-footprint gradient baseline in PyTorch. |
| `run_phase0.sh`, `run_phase2.sh` | The baseline and control runs, in order. |
| `runs/p0_*`, `runs/p2_*` | Their outputs: `summary.json` and `results.jsonl` per run. |
| `ref/` | The report's released prompt, Codex configuration and experiment README, for comparison. |
| `PLAN.md` | The plan as it evolved, including what was cut and why. |

Large files are not in the repository: model checkpoints, datasets, rebuilt edited checkpoints, and the activation dumps the editor requested (`runs/*/work/fwd_*`). The turn logs reference them by path.

## Run your own session

```bash
python harness/driver.py --run runs/my_run --passes 25 --protocol think --editor fable
```

`--editor fable` calls the Claude Code CLI headless (`claude -p`) with tools, settings and memory off; `--editor codex` calls the Codex CLI with `gpt-6-astra`, the report's editor. A session is resumable: rerun the same command and it continues from `state.json` with a handoff. One session is about 10 hours on an M-series laptop, most of it forward passes.

## Status

Done: Phase 0 baselines, one Fable session, held-out evaluation, template-flag, random-location and gradient controls, paper draft. Running: a second Fable session. Next: two GPT-6 Astra sessions, an ablation map over every attention head and MLP block, then the arXiv submission.
