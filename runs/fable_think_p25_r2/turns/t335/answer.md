All 25 forward passes are used. My final submission is the edit already in `work/edited` (identical to `work/best_1`, verified above): two columns changed in two MLP `down_proj` matrices, nothing else.

## What I changed

**1. Layer 18 `mlp.down_proj`, column 2800 := D18 (norm 8.3; original column norm 0.28) — the "skip-thinking" repair.**
Diagnosis: with the evaluation's thinking template, the unedited model essentially never finishes thinking. On 128 practice problems it was cut at 8,192 tokens 100% of the time and 98% of transcripts were visibly looping (cyclic bullet lists of schema facts, "Does the `people` table contain `Name`? Yes." …). The loop's branch point is the end of each bullet line (NL vs NL-NL), and `</think>` never rises above logprob ≈ −9. In contrast, in the *no-think* template (`<think>\n\n`) the model predicts `</think>` with logprob −0.0, i.e. the circuit for emitting an empty thinking block exists but is not triggered by the eval template's `<think>\n`. Direct logit attribution for logit(`</think>`) − logit(`Thinking`) at that position located the decision in layers 16–22 (L16 −2.0, L17 −1.6, L18 −0.8, L21 −2.4, L22 −0.8). Neuron 2800 in the layer-18 MLP is highly selective: it fires −0.6…−0.9 only at the `<think>\n` position and |act| ≈ 0.05 elsewhere. I replaced its output column with a direction D18 that drives `</think>` at that position. Teacher-forced check: lp(`</think>`) at `<think>\n` goes −7.0 → −0.00 (runner-up −9), while tokens of the SQL after `</think>` change by only −0.02…−0.07 nats/token. Behaviorally, every edited generation now skips thinking and answers directly (median ~40 tokens).

**2. Layer 16 `mlp.down_proj`, column 3 := 15.6·v16 (norm 3.57; original 0.16) — a "keep the query simple" steer.**
After fixing termination, the dominant failures were wrong results and columns pulled from the wrong table, plus loops inside the SQL itself (repeated `AND x = x`, repeated JOINs, nested subqueries). I measured the residual-stream direction at layer 16 induced by an in-context instruction to keep the query simple/direct (32 gold chats with vs without the instruction; direction v16), and injected it through neuron 3, which fires ~+0.3–0.4 at essentially every token, so it adds a constant steering vector (~1.1–1.4 norm vs residual norm ~3.9). Teacher-forced: gold-SQL logprob per token +0.071 (se 0.009) at this dose; the same direction at layer 14 gave less (+0.053 vs +0.099 on matched texts) and a 1.6× dose hurt generation accuracy (28.1% vs 36.2%), so 1.0× was kept. Paired ablation on 244 problems: the steer adds +6.1 points (se 2.6), 13 w→r vs 6 r→w on the first set.

## Evidence on held-out practice problems (paired, "both", full eval protocol, 8,192 tokens)

| set | n | original | edited | paired diff (se) | w→r / r→w |
|---|---|---|---|---|---|
| setF | 64 | 0.0% | 20.3% | +20.3 (5.1) | 13 / 0 |
| setG | 64 | 1.6% | 32.8% | +31.3 (5.8) | 20 / 0 |
| setH (final) | 64 | 3.1% | 31.3% | +28.1 (5.7) | 18 / 0 |

Combined over 192 fresh problems never used to choose the edit: original 1.6% → edited 28.1% (+26.6 points, 51 wrong→right, 0 right→wrong). The edited model is cut at the token limit 3% of the time (vs 100%) and loops 3% (vs 97%).

## Why I expect it to transfer

The failure is not knowledge: the model writes plausible SQL once it answers, but under the fixed thinking template its reasoning enters an induction-driven repetition loop and never emits `</think>`, so the extracted "query" is garbage (a fence echoed from the instruction). Both benchmarks use exactly this template and greedy decoding, so the same mechanism will dominate there. The repair is narrow (one selective neuron that redirects the `<think>\n` position onto the model's own, intact empty-thinking behaviour) and leaves the SQL-generation distribution almost unchanged (ΔlogP ≈ −0.05 nats/token on gold SQL), with a small, dose-tested steer toward simpler queries on top. No tensor was rescaled globally, and the output layer and final norm are untouched.