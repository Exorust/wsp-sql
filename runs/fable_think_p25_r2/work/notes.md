# Notes (fable_think_p25_r2)
## Diagnosis (gen_1, 128 Spider-train problems, original model, 8192 max tokens)
- accuracy 4.7%, 100% cut at max tokens, 97.7% looping. Loops start at answer token ~90-600 (median ~chars 1800),
  periods 35-120 tokens: cyclic bullet lists of schema facts ('*   The `X` table has `Y`.', 'Does the `people` table contain `Name`? Yes.',
  '*Wait, is there a specific constraint on ...?*'). Never emits </think>. The 6 'correct' are flukes (first SELECT inside thinking).
- Core problem = thinking never terminates due to repetition loops.
## Attention analysis (fwd_2: 2 loop texts, attn patterns of layers 3,7,11,15,19,23)
- Induction heads (mass on earlier copies of NEXT token, loop vs pre-loop): L11h1 0.53-0.63 vs 0.27-0.32; L15h7 0.70-0.73 vs 0.41;
  L23h5 0.55-0.71 vs 0.35; L23h4 0.34-0.48 vs 0.28; L23h0 ~0.4 vs 0.2; L19h5/6/7 ~0.35 vs 0.2.
- Duplicate-token heads (mass on earlier copies of CURRENT token): L3h7 0.8, L3h4 0.4, L7h5/6/7 ~0.6, L11h3 0.36, L23h6 0.8.
- Loop logprobs: rep0 mean -0.13/-0.49, rep2 -0.02 (locks in). </think> at ~-12.
## Forward passes used: 2 (gen_1 diagnostic; fwd_2 attn)

## Session 2 (kernel restarted at turn 52)
- Current edit = zero o_proj head slices L11h1, L15h7, L23h5 (induction heads). fwd_3 (orig) vs fwd_4 (edit) on 6 loop texts + 16 gold chats:
  loop-region logprob -0.13..-0.19 nats/token; pre-loop -0.07; gold SQL tokens -0.08 nats/token (hurts slightly). Did not flip any greedy decision.
- KEY FINDING (fwd_3 topk): the loop's branch point is the end of each bullet line: NL (continue list, id 198) vs NLNL (end section, id 271).
  In loop regions logP(NLNL) is -0.7..-3 (near tie) while NL wins; pre-loop lists have NLNL at -5..-8. </think> is ~-9.
- gen_1: only 38/128 texts contain any SELECT; 120 contain a sql fence only because the thinking echoes the instruction -> 'syntax' class is an artifact.
- fwd_5 (12 loop texts, all hidden states + mlp acts). DLA of logit(NLNL)-logit(NL) at decision positions:
  layer 23 (last) writes essentially everything: pre-loop cont. -7.0, loop cont. -2.0, section-end +5.2; layers 0-22 ~0 each.
  Inside layer 23: attention -7.15/-2.05/+5.38, MLP ~0.1. => the last full-attention layer's heads decide list continuation.
  Final norm uses (1+w) convention (verified: slope 0.97 vs logprob diffs).
- JSON for forward blocks: escape backticks as \u0060 (a literal triple backtick ends the block). Never put triple backticks in code blocks either.

## Session 3 (kernel restarted at turn 132; 8 passes used)
- gen_7 (edited = zero L23h5 o_proj slice): acc 0.8%, 100% cut, 96% looping -> zeroing L23h5 does NOT help. (edit still in /edited; to be dropped)
- CORRECTION: hidden_L24 from the tool is the POST-final-norm vector (logits = E @ hidden_L24, err 0.04; treating it as pre-norm gives err 0.55).
  hidden_L23 = input to the last layer (layer index 23). So the earlier "layer 23 writes everything" DLA was an ARTIFACT. Residual RMS ~0.3 at layers 20-23, 4.4 post-norm.
  Correct DLA at the '<think>\n' position for logit(</think>)-logit(Thinking) (total -6.5): layers 16 -2.0, 17 -1.6, 18 -0.8, 21 -2.4, 22 -0.8, 23 -0.5; early layers ~0.
- KEY: in the no-think template '<think>','\n\n' the model predicts </think> with logprob -0.0; at '<think>' it splits '\n' -0.63 / '\n\n' -0.76.
  In the eval template ('<think>','\n') it predicts 'Thinking'(-0.17) and </think> at -7.3. In the model's own traces </think> never exceeds ~-9.
  Progress in gen_1: loop starts in section 2/3 (Analyze the Schema / Identify the Goal) for 84/128; only ~20 reach 'Formulate the Query'; even those loop ('Okay, I will output the query. Wait, ...').
- PLAN: retarget the empty-thinking circuit so that '<think>','\n' -> </think> (skip thinking), by editing the neurons/heads that implement it.

## Session 4 (kernel restarted at turn 172; 10 passes used)
- Reconstructed: passes 8-10 were teacher-forced. fwd_9 (orig): T1 = no-think template (<think>\n\n</think>), T2 = eval template with immediate </think>,
  T3 = short thinking then </think>, T4 = model-style thinking then </think>. fwd_10 (edited) = 8 T2 texts.
- CURRENT EDIT: L18 mlp down_proj column 2800 := D18 (work/D18.npy, norm 8.29; original column norm 0.28). Neuron 2800 fires -0.6..-0.9 ONLY at the
  '<think>\n' position (prediction of </think>); elsewhere |act| ~0.05 (max 0.25-0.34). Effect (fwd_10 vs fwd_9): lp(</think>) at '<think>\n' goes
  -7.0 -> -0.00 (runner-up at -9); SQL tokens after </think> change by only -0.02..-0.07 nats/token. => model should skip thinking and answer directly.
- gen_1 classes: {"syntax": 119, "correct": 6, "cut_no_sql": 3}
- NEXT: generation pass of EDITED model on the same 128 ids as gen_1 (orig baseline 4.7%) to measure real accuracy of skip-thinking.

## Session 5 (kernel restarted at turn 212; 12 passes used)
- gen_11 (EDITED skip-thinking, same 128 ids as gen_1, max_tokens 2048): accuracy 27.0% (orig 4.7%), mean 257 tokens, 10% cut, 8% looping.
  failures: wrong_result 50, no_such_column 29, other_error 6, ambiguous 3, syntax 2, ungraded 2, misuse 1, timeout 1.
- fwd_12 (edited): teacher-forced 36 gold chats (ids in tf12_meta.json) with hidden states L0-24 and mlp acts L12-20+ (for SQL-failure analysis).

## Session 6 (kernel restarted at turn 292; 16 passes used)
- Reconstructed passes 13-16: fwd_13 = 64 teacher-forced texts (32 gold chats base + 32 with INSTR1 'keep query simple'), hidden L10-18 -> v16 = instruction direction at L16 (norm 0.229).
  L16 EDIT: down_proj column 3 := 15.6*v16 (norm 3.57; neuron 3 fires +0.3..0.4 at ~all tokens => constant steering ~1.1-1.4 norm vs resid norm 3.9).
  fwd_14/15 (two strengths) vs fwd_13 baseline: gold-SQL lp/token +0.071 (se 0.009) and +0.123 (se 0.020).
- gen_16 (L18+L16, 128 NEW ids): acc 33.6%, 7.8% cut, 7% loop; failures wrong_result 48, no_such_column 26 (mostly column from wrong table), other 4, ambiguous 4.
  10 cut answers = loops INSIDE SQL ('AND Campus = Campus' repeated, repeated JOIN lines, nested subqueries, repeated select columns).
- best_1/ = L18+L16 edit. gen_17 = L18-only on gen_16 ids (paired ablation of L16).
- gen_17 (L18 only, gen_16 ids, 116 overlap): acc 30.2% vs 36.2% with L16 => L16 steer +6.0 (se 3.7), 13 w->r, 6 r->w. gen_18 (L16 x1.6): 28.1% => overshoot hurts; x1.0 (15.6*v16) kept. best_1 = current.
- setC (128 fresh ids, work/setC.json): gen_19 L18+L16 = 33.6%, gen_20 L18-only = 27.3%; paired diff +6.2 (se 3.6). Combined B+C n=244: +6.1 se 2.6. L16 steer KEPT (x1.0). Current edited = best_1.
- fwd_21: in-context gold-lp gains on 12 short chats: INSTR1 +0.075; INSTR2 (exact names) -0.021; INSTR3 (join rule) -0.139; INSTR4 (exact columns) -0.034 => no new steering direction worth injecting.
- fwd_22: INSTR1 direction injected at L14 (neuron 1391, same relative dose): gold-lp gain +0.053 (se 0.040) < L16 steer +0.099 (se 0.024) on same 12 texts => L16 kept, L14 dropped.
- FINAL EDIT = best_1: L18 down_proj col 2800 := D18 (skip-thinking) + L16 down_proj col 3 := 15.6*v16 (simplicity steer). gen_23 = both on 64 fresh ids (setF.json), max_tokens 8192.
- gen_23 (both, 64 fresh ids setF, 8192 tok): original 0.0% (100% cut, 94% looping) vs edited 20.3%; paired +20.3 (se 5.1), 13 w->r, 0 r->w; all 64 edited answers skip thinking (median 40 tokens).
- gen_24 = both on setG (64 more fresh ids).
- gen_24 (both, 64 fresh ids setG, 8192 tok): original 1.6% vs edited 32.8%; paired +31.3 (se 5.8), 20 w->r, 0 r->w.
  COMBINED final confirmation (128 fresh problems): original 0.8% -> edited 26.6% (+25.8 points, 33 w->r, 0 r->w).
- SUBMITTED: work/edited = best_1 (L18 col 2800 skip-thinking neuron + L16 col 3 simplicity steer). 24/25 passes used.

## Session 7 (kernel restarted at turn 332; 24 passes used, 1 code run left)
- Verified work/edited == best_1 (see output). setH.json = 64 fresh ids for the last paired confirmation (gen_25, both).
- FINAL: work/edited = best_1 unchanged.
