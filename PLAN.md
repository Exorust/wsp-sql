# WSP-SQL: weight-space programming for Qwen on text-to-SQL

Started 2026-11-04. Replicates "Sparks of Weight-Space Programming" (Takehi, Teoh, Zhang, Khattab, MIT CSAIL, 2026-11-02) with SQL instead of math.

Weight-space programming (WSP): a frontier LLM gets a Python kernel over a small model's weights, a budget of forward passes on practice problems, and a goal in plain English. It edits weight values directly. No gradients, no training.

## What the original actually showed, and why it matters here

- The whole MATH-500 gain (7.9 to 48.1) came from one repair: Qwen3.5-0.8B with thinking on loops until the 32,768-token limit on 93% of problems. Astra found the "loop direction" written by the MLPs of layers 15 and 19 and subtracted it from 64 columns of `down_proj` in each (131,072 weights).
- The authors' own follow-up on Gemma 3 270M, which does not loop, gained nothing (6.8 to at most 7.7). Their words: editing "could remove an obstacle that hid an ability, but it could not add an ability the model lacked."
- So the method is a debugger, not a trainer. For SQL it will work only if the small model has a localized failure mechanism that hides SQL ability it already has. Whether such a mechanism exists is the first question, and it is cheap to answer.

Risk stated plainly: text-to-SQL failures in small models are mostly schema linking and wrong semantics (the soql-expert baseline on Qwen3-4B found date format, SOSL syntax and arithmetic as the top causes). Those are knowledge gaps, not obstacles. A null result is likely and is still a publishable finding, since nobody has tested WSP outside math yet.

## Phase 0: is there an obstacle to remove? (laptop, one session)

Benchmark: BIRD Mini-Dev, 500 questions over 11 SQLite databases (`data/bird_minidev/minidev/MINIDEV/`). Metric: execution accuracy (predicted and gold SQL return the same result set). Spider dev (1,034 questions) is the second benchmark; its databases are not on Hugging Face, download from the Yale site later.

Runs, all on the same 500 questions, greedy or the model card's sampling:

| Model | Thinking | Max new tokens |
|---|---|---|
| Qwen/Qwen3.5-0.8B base | off | 1,024 |
| Qwen/Qwen3.5-0.8B base | on | 8,192 |
| RikiyaT/Qwen3.5-0.8B-weight-space-programming (the math edit) | off | 1,024 |
| RikiyaT/Qwen3.5-0.8B-weight-space-programming | on | 8,192 |

For every answer record: correct, wrong result, SQLite execution error (by error class), no SQL emitted, cut at the token limit. Keep the texts.

Decision gate: build the harness only if one explainable non-semantic failure class (loops, truncation, no SQL emitted, one recurring syntax habit) covers at least 25% of failures. If the math edit alone already moves SQL accuracy, that is a result in itself (the loop fix transfers across domains).

Cost: about 1.6 GB download per model, 2,000 generations total on an M5 with mlx-lm, roughly 1 to 3 hours. Not a heavy GPU run.

## Phase 1: the harness (only if the gate passes)

The authors released logs and prompts but not the harness code. Copies of what they did release are in `ref/` (first-turn prompt, Codex config, sandbox sketch, exp8 README). Three pieces to write, about 400 lines total:

1. **Kernel.** A persistent Python process over the weights with `NAMES`, `load`, `load_original`, `save_edit`, `drop_edit`, `edited`, `tok`. `save_edit` refuses the final norm, embeddings, lm_head and whole-tensor constant multiplies. No bubblewrap on macOS: run it as a subprocess with `python -I`, a time limit and a memory limit, and accept weaker isolation.
2. **Forward-pass server.** Generation (up to 512 items, original/edited/both with paired difference and standard error, SQL grading by execution) and teacher-forced reads (log-probs, hidden states, MLP activations). mlx-lm for generation, transformers on MPS for activations. Budget 25 or 50 passes. Practice set: BIRD train (9,428) and Spider train (7,000), never Mini-Dev or Spider dev.
3. **Driver.** One `codex exec` per turn with `gpt-6-astra`, reasoning effort max, all Codex tools off (their config is `ref/harness/codex_config.toml`), exactly one ```python or ```forward block per reply, a fresh conversation with a handoff message every 40 turns.

The first-turn prompt is `ref/exp8_math/runs/p50c/turns/t001/prompt.txt` with math swapped for SQL and the measurement protocol changed to execution accuracy on a held-out set.

## Phase 2: run and evaluate

- One 25-pass run first, then 50 if it moves. The original 50-pass run took 20 wall-clock hours, most of it forward passes. On the laptop a generation pass of 512 SQL answers at 1,024 tokens is well under an hour; with thinking on it is several hours. If thinking mode is the target, rent a GPU for the forward-pass server (Modal, as in the kernel work).
- Evaluate base, our edit and the math edit on Mini-Dev and Spider dev.
- Required control: the same base model with a decoding fix only (repetition penalty, lower max tokens, thinking off). If the edit only removes loops, this control gets the same gain for free. That is the criticism raised against the original, so it has to be in the table.

## Decisions for the user

1. Target: Qwen3.5-0.8B on SQL (this plan) or Qwen3-4B on SOQL (the soql-expert project). Recommendation: 0.8B on SQL first. Phase 0 costs almost nothing and the only demonstrated WSP win needs thinking mode, which 0.8B has.
2. Where forward passes run: laptop (free, slow with thinking on) or Modal GPU (fast, paid).
3. Measured protocol: thinking on or off. Thinking off is what SQL deployments use; thinking on is where loops live.

## Layout

```
PLAN.md            this file
ref/               released prompt, Codex config, sandbox sketch, exp8 README, apply_edit.py, profiles.py
data/bird_minidev/ BIRD Mini-Dev (500 questions, 11 SQLite databases, 1.4 GB)
.venv/             Python 3.11, torch 2.15 (MPS), transformers 5.22, mlx-lm
```

## Paper plan (2026-11-06)

Question: does an agent that reads weights beat gradient descent on the same weights, and does the answer depend on the agent?
Arena A = text-to-SQL (this repo). Arena B = the report's math setting, Astra arm = the released run `p25c`. 2026-11-06: Arena B is deferred; Arena A first.

| Arm | Arena A (SQL) | Arena B (math, thinking on) |
|---|---|---|
| Fable, 25 passes, 2 runs | `harness/driver.py --editor fable` | needs a math grader + prompt in the harness; passes on Modal or an 8,192-token cap |
| Astra, 25 passes, 2 runs | `harness/driver.py --editor codex` | released `p25c` (1 run) |
| Gradient, same footprint | `baseline_sft.py --footprint <agent's edited_model>` on Spider train gold SQL | same loci (64 cols of down_proj L15/L19); data = self-distilled correct traces |
| Controls | base, repetition penalty 1.2, released math edit | base, released math edit |

Held-out: BIRD Mini-Dev + Spider dev (A); MATH-500 + GSM8K + IFEval (B). Paired differences only.
Transfer of the math edit to SQL and the semantic-failure null become baseline rows, not headline results.
Fable usage is on the Claude plan (not billed per token).
