Final choice: the edit currently in `/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r1/work/edited` (identical to `best_1`, "v2") is submitted.

## What I changed

Four `down_proj` columns in the MLPs of layers 17–20 — one neuron per layer:

| layer | neuron | added to its down_proj column |
|---|---|---|
| 17 | 537 | 0.20 · u |
| 18 | 628 | 0.20 · u |
| 19 | 2424 | 0.25 · u |
| 20 | 1235 | 0.15 · u |

where u is the unit vector of (final-norm gain ⊙ unembedding row of `</think>`), i.e. the residual-stream direction that the tied output layer reads out as the `</think>` token. Nothing else is touched; the final norm and embeddings are unchanged, and no tensor is globally rescaled.

## What was going wrong (diagnosis)

- The unedited model is essentially useless under the evaluation protocol: on 128 diagnostic problems, 1.6% accuracy, 99% of answers cut at 8,192 tokens, 95% visibly looping, only 1/128 ever reached `</think>`. It writes "Thinking Process: 1. Analyze the Request … 2. Analyze the Schema …" and then repeats bullets like "*   The `Dorm` table has `gender`." forever. The loop sets in early (median ≈290 generated tokens), before any SQL is drafted.
- Teacher-forced probes showed the loop is "soft" (copy token wins by only 1–2 nats at each bullet start/end; L23 digit-suppressor neurons tip the section-advance decision toward another indented bullet), but interventions on the induction heads (zeroing o_proj columns of L15h7/L11h1/L23h5/L19h5) and on the L22/L23 bullet/digit neurons did not stop the loop (both 100% cut). The looping is distributed and not fixable at one site.
- The decisive observation: at the first thinking position (right after `<think>\n`), `</think>` is already a plausible continuation at log-prob −6.9 (rank 6–8), with MLPs L16–23 diffusely pushing against it. Four neurons fire selectively at exactly that position and nowhere else (activations 1.2–2.7 there; 99.9th percentile elsewhere ≤0.3–0.7): L17n537, L18n628, L19n2424, L20n1235. They are a clean "start-of-thinking" detector, so making them write the `</think>` direction acts only at that one decision point.

## Effect and evidence

- Teacher-forced (fwd_10): at the first thinking position lp(`</think>`) goes from −6.9 to −0.11…−0.24; robust to a 4,196-token prompt (−0.12) and to BIRD-style "Hint:" prompts. After `</think>` the model proceeds normally to a ```sql block (median ≈47 tokens on short problems).
- Paired generation vs the original on fresh, unused problems, seven independent 64-problem sets (gen_18, 20–25; n = 448 total): original ≈1.1% accuracy, edited ≈28%; paired difference +26.8 points overall (per set +18.8 to +31.3, each 3–5 standard errors above zero); 122 problems went wrong→right, 2 went right→wrong. Cut-off answers drop from ~100% to 3–16%.
- Remaining failures (no_such_column ~25%, wrong_result ~35%) are genuine SQL errors — question words used as column names, missing joins — and are the model's underlying capability, not an artefact of the edit; I probed them (fwd_17) and found the bias lives in attention/early layers with no neuron-level handle.

## Why I expect it to help on the held-out benchmarks

The mechanism is prompt-independent: the detector neurons respond to the `<think>\n` boundary that the fixed chat template always produces, the edit only adds a readout-direction vector at that single token, and the behaviour (skip the degenerate "Thinking Process" loop and answer directly) was confirmed on 448 unseen Spider-train problems with a BIRD-style Hint format checked as well. Since the unedited model almost never finishes within 8,192 tokens, converting those to completed queries at ~28% accuracy should transfer to both Spider dev and BIRD Mini-Dev.