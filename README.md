# When AI debugs AI: repair or bypass?

An independent test of the claim in MIT CSAIL's *Sparks of Weight-Space Programming* (Takehi, Teoh, Zhang, Khattab, 2 November 2026): that a frontier language model, given a small model's weights and a budget of forward passes, can find why the small model misbehaves and fix it by editing the weights directly, with no training.

Same small model as the report, Qwen3.5-0.8B. A new task, text-to-SQL. A new editor, Claude Fable 5.1, in two independent sessions. The full trace of what the editor tried, the edits it submitted, held-out numbers, and controls.

The finding: "the bug is gone" can mean two different things, and one cheap measurement tells them apart.

- **Paper (draft):** [paper/main.pdf](paper/main.pdf)
- **Blog post:** [charoori.com/blog/weight-space-programming-sql](https://charoori.com/blog/weight-space-programming-sql)
- **Interactive explainer:** [wsp-sql.vercel.app](https://wsp-sql.vercel.app)

## The result

With thinking enabled, Qwen3.5-0.8B writes its reasoning between a `<think>` tag and a `</think>` tag before it answers. On SQL questions that reasoning repeats itself until the token limit on 91% of questions, and 0.7% of answers are correct. An edit can make this go away in two ways:

- **Repair.** The model still reasons, and the reasoning now ends.
- **Bypass.** The model writes `</think>` at once and skips reasoning. The chat template already has a flag that does this.

Both Fable sessions removed the loop, with 4,083 and 2,048 changed weight entries on different neurons, and random-location edits of the same size do nothing. But both edits are bypasses, and neither beats the template flag. Session 1 first tried two repairs built from measured hypotheses about the loop (induction heads; digit-suppressing neurons in the last layer), and both failed. Gradient descent restricted to the same entries finds the same bypass.

| Condition (BIRD Mini-Dev, 150 q, greedy, 8,192 tokens) | Correct | Cut at limit | Looping |
|---|---|---|---|
| Base, thinking on | 0.7% | 98.7% | 90.7% |
| Base, thinking off via template | 7.3% | 12.0% | 10.7% |
| Report's math edit | 3.3% | 87.3% | 82.0% |
| Fable session 1 edit (4,083 entries) | 6.0% | 27.3% | 26.0% |
| Fable session 2 edit (2,048 entries) | 5.3% | 25.3% | 24.0% |
| Random location, session 1 size, 5 draws (50 q each) | 0 to 2% | 100% | 90 to 98% |
| Random location, session 2 size, 5 draws (50 q each) | 0 to 4% | 94 to 100% | 86 to 96% |
| Gradient descent on session 1's entries | 4.7% | 30.7% | 29.3% |
| Gradient descent on session 2's entries | 7.3% | 29.3% | 29.3% |

The measurement that separates the two outcomes is how much text comes before `</think>`:

| Condition (same 150 questions) | Answers that close thinking | Of those, with zero reasoning | Median characters of reasoning |
|---|---|---|---|
| Base | 2 | 0 | 3,092 |
| Report's math edit | 22 | 0 | 5,768 |
| Fable session 1 edit | 150 | 150 | 0 |
| Fable session 2 edit | 150 | 150 | 0 |
| Gradient descent, either footprint | 150 | 150 | 0 |

Under greedy decoding the report's math edit helps little on SQL, but where it works it is a repair. Every edit found on SQL is a bypass.

### The same edits under the report's sampling settings, and on math

The tables above use greedy decoding. The report samples: temperature 0.6, top-p 0.95, top-k 20, presence penalty 1.5. With those settings, on the same 150 SQL questions (`run_phase3.sh`):

| Condition (BIRD, sampled, 8,192 tokens) | Correct | Cut at limit | Close thinking | Of those, zero reasoning | Median characters of reasoning |
|---|---|---|---|---|---|
| Base, thinking on | 5.3% | 75.3% | 37 | 0 | 9,851 |
| Base, thinking off via template | 6.7% | 0.7% | n/a | n/a | n/a |
| Report's math edit | 10.7% | 8.0% | 139 | 0 | 16,146 |
| Fable session 1 edit | 2.0% | 4.7% | 144 | 140 | 0 |
| Fable session 2 edit | 2.7% | 0.7% | 150 | 150 | 0 |

This corrects the greedy picture: with its own sampling settings the math edit removes most of the SQL loop, and it does so as a repair, after a median of 16,146 characters of reasoning. Greedy decoding hid that. The accuracy gaps are 16, 10 and 8 correct answers of 150 and are not significant.

On 100 MATH-500 problems (thinking on: sampled as above, 16,384 tokens; thinking off: model-card settings, 8,192 tokens):

| Condition (MATH-500, 100 problems) | Correct | Cut at limit | Close thinking | Of those, zero reasoning |
|---|---|---|---|---|
| Base, thinking on | 8% | 92% | 8 | 0 |
| Base, thinking off via template | 42% | 33% | n/a | n/a |
| Report's math edit | 21% | 72% | 28 | 0 |
| Fable session 1 edit | 9% | 91% | 9 | 0 |
| Fable session 2 edit | 9% | 89% | 13 | 0 |

The Fable edits do nothing on math: no answer closes thinking at once and the loop stays. The bypass is tied to the SQL prompt; the repair carries over from math to SQL. The math edit's 21% is below the published 48% because our limit is 16,384 tokens, not 32,768, and 72 of 100 answers still hit it.

Whether an editor can find a repair on SQL directly is the open question; two GPT-6 Astra sessions on SQL are next.

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
| `runs/fable_think_p25_r1/`, `runs/fable_think_p25_r2/` | The two editing sessions (r1 has 328 turns, r2 has 335). `turns/t001` to `t328`: every prompt and reply. `work/notes.md`: the editor's own notes. `final_answer.md`: its submission. |
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

Done: Phase 0 baselines, two Fable sessions, held-out evaluation, template-flag, random-location and gradient controls for both, paper draft. Next: two GPT-6 Astra sessions, an ablation map over every attention head and MLP block, then the arXiv submission.
