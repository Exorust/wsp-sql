# Notes

## State
- 3/25 forward passes used (pass 3 WASTED: "texts": "@@FILE" is not allowed; JSON must be inline in the forward block; kernel output cut at 10k chars so print in chunks).
- Code cannot contain triple backticks (block ends); use FENCE = "`"*3.

## Findings
- gen_1 (original, 128 diag problems, 8192 tok): accuracy 1.6%, 99% cut at max tokens, 95% visibly looping. Only 1/128 reached </think>.
  The model writes "Thinking Process: 1. Analyze the Request ... 2. Analyze the Schema ..." then loops on bullets like
  "*   The `Dorm` table has `gender`." or "*   Does the `entrepreneur` table have `X`? Yes." forever.
- fwd_2 (teacher-forced, 2 loop texts, attention at 3,7,11,15,19,23): in the loop region, induction heads (mass on t+1-period):
  L15h7 0.26 (+0.17 on 2 periods back), L11h1 0.10, L23h5 0.12, L19h5 0.08, L23h7 0.08, L23h4 0.07, L23h0 0.06. L23h2 is a self-attention head (0.58).
- Loop is SOFT: at bullet start (after "*  ") p(' The')~0.35-0.58 vs ' So' ~0.12, ' Wait' ~0.05-0.13; after bullet end, p('\n\n')~0.1-0.25 (would start a new section).
  Margin ~1-1.5 nats. Greedy always picks the copy token.

## Files
- splits.json: diag (128 ids used in gen_1), confirm_pool (2000 ids unused).
- setA.json: 119 loop texts (raw rendered, thinking inside <think>, truncated after a few periods) with 'onset','period' in tokens.
- setB.json: 200 gold-SQL texts rendered with empty thinking.
- req3.json: the 319-text request (too big to paste inline; 1MB).

## Edits tried
(none yet)

- fwd_4 (pass 4, original): 16 loop texts (setA shortest) + 24 gold texts (setB shortest). Loop decision points (n=79 bullet-starts, 75 bullet-ends in loop region):
  copied token lp mean -0.46 (start) / -0.22 (end); best alternative ('Wait' at starts, '\n\n' at ends) lp mean -2.5/-2.3; median margin 1.6/1.9 nats.
  fwd_2 attention: L15h7 schema-section attends 0.44 prompt/0.53 own text, in loop 0.42 induction; L11h1 0.70 prompt / 0.20 induction. Induction heads also serve schema copying.
- Probe B (pass 5 planned): zero o_proj columns of L15h7, L11h1, L23h5, L19h5.
- Forward JSON must escape triple backticks as \u0060\u0060\u0060 (else the block ends early). req4_edited.json holds the probe request.

## Passes 5-7 (recovered after kernel restart)
- Pass 5 (TF edited, probe B = zero o_proj cols of L15h7,L11h1,L23h5,L19h5): see fwd_5.
- Pass 6 (gen both, 40 problems): original 2.5% (1/40), edited 0% (0/40); both 100% cut, looping 90%/100%. Probe B FAILED -> dropped.
- Pass 7 (TF original, 6 texts ~1600 tok: model's own loop transcripts), hidden L8,12,16,20,22,23 + mlp down_in L16-23 saved in fwd_7.
- 7/25 passes used at restart.

## Key finding (pass 7 analysis)
- Section-advance decision after '\n\n' (indent '   ' vs next section digit) has margins 0.4-2.5 nats in loop texts.
- Final-layer MLP (L23) has DIGIT-SUPPRESSOR neurons that fire when a digit is about to be predicted and demote exactly that digit by ~3 nats:
  n580('3'), n598('5'), n564('4'), n557('1'), n485('2'), n669('6'), n639('7'). They tip the balance to indentation -> model keeps adding bullets.
- Bullet-end decision ('\n' vs '\n\n'): soft points (margin<3) ~25%; neurons L22n817, L23n879, L23n935 push toward '\n\n' (fire at '.', '`', ')').
- L22n796: generic indent promoter active at newlines (+2..3.6 nats toward indent at '\n\n').
## Edit v1 (saved): L23 zero cols {580,598,564,557,485,669,639}; L23 x2 {879,935}; L22 x0.5 {796}; L22 x2 {817}. Testing with TF pass 8 on pass-4 texts.

## Session 3 (passes 10-11)
- v1 edit (L22/L23 neuron scalings) had no effect on looping (pass 9: both 100% cut; 0% vs 2%). DROPPED.
- Loops start early (median 290 generated tokens); only 16/90 loop texts had any SELECT before onset. Model never reaches an answer.
- At first thinking position (after '<think>\n'), </think> is at lp -6.9 (rank 6-8); 'Thinking' wins. DLA: MLPs L16-23 push against </think> by ~9 nats, diffuse.
- Found selective START-OF-THINKING detector neurons (fire only at the '\n' after <think>): L17n537 (1.53), L18n628 (1.55), L19n2424 (1.17), L20n1235 (2.74); |rest| p99.9 <= 0.3-0.7.
## Edit v2 (CURRENT BEST, saved in best_1): add alpha*u (u = unit(gN*E[</think>])) to down_proj columns: L17n537 a=0.20, L18n628 a=0.20, L19n2424 a=0.25, L20n1235 a=0.15.
- fwd_10 (TF edited, 8 direct-format texts): lp(</think>) at first pos = -0.11..-0.24 (was -6.9); 'Thinking' second at ~-2.1. after </think>: '\n\n' p=1.
- gen_11 (edited, 64 problems genA+genB[:24]): accuracy 29.7% (19/64) vs original ~1%; all 64 answers start '</think>\n\n'; median 47 tokens; 5/64 cut (answer-region loops: repeated AND clauses / repeated column); failures: wrong_result 26, no_such_column 14 (column attached to wrong table alias / missing join), other 4, no_such_table 1.

## Session 4 (passes 12-16)
- gen_12 (v2, 128 problems): 27.3%; failures wrong_result 42, no_such_column 39 (model writes question-wording columns e.g. film.id, team.id, year instead of film_id/team_id/yearid), other 9, misuse 3; 15 cut (answer loops).
- v3 = same 4 neurons writing unit(gN*E['Okay']) (start free-form thinking): gen_16 on 64 of gen_12 ids: 3.1%, 98% cut, 94% looping. FAILED -> reverted to v2 (best_1).
- Code runs very limited (~28 left).

## Session 4 cont. (passes 17-18)
- fwd_17 (TF v2, 19 short no_such_column cases + 10 correct): at the hallucinated-column decision token, a valid schema column is 2nd at median margin 1.1 nats; MLPs L16-23 contribute ~0 (|sum|<0.3) to the wrong-over-valid logit diff -> the bias is in attention/earlier layers (copying question words: ' city',' dew','.Car','Name', or right column/wrong table). No neuron-level fix found; not pursued (code runs exhausted).
- fwd_14: with a 4196-token prompt, lp(</think>) at first thinking pos = -0.12 (robust to long schemas); gen_12 long prompts (>1500 tok): 5/22 correct, all skip thinking.
- gen_18 FINAL CONFIRM (both, 64 fresh ids from confirm_pool, gen_sets_confirm.json): original 0/64 (100% cut, 97% looping); v2 17/64 = 26.6%; paired diff +26.6 +- 5.6 pts, 17 wrong->right, 0 right->wrong. v2 failures: no_such_column 28, wrong_result 13, other 4, syntax 2; 8 cut (answer loops).
- FINAL CHOICE: v2 (edited == best_1).

## Session 4 final (passes 19-21)
- gen_19 (edited, confirmB 64 fresh + 3 BIRD-style Hint prompts): 23/64=35.9%; Hint prompts all skip thinking and give SQL (25-56 tokens).
- gen_20 (both, confirmC fresh): orig 1/64, v2 13/64; paired +18.8 +- 5.4 (13 w->r, 1 r->w).
- gen_21 (both, confirmB): orig 2/64, v2 22/64; paired +31.3 +- 5.8 (20 w->r, 0 r->w).
- Combined fresh paired (gen_18,20,21; n=192): +25.5 pts, 50 wrong->right, 1 right->wrong. FINAL = v2 (edited == best_1 == best_final).

## Session 5 (passes 22-25 planned)
- Kernel restarted; edited==best_1 verified: True. Fresh sets confirmD0-3 (64 each) in gen_sets_confirmD.json for extra paired confirmation of v2.
- gen_22..25 (both, confirmD0-3, 64 fresh each): orig 2/64,0/64,1/64,0/64; v2 19/64,19/64,21/64,15/64;
  paired +26.6+-5.6, +29.7+-5.8, +31.3+-6.3, +23.4+-5.3; wrong->right 17,19,21,15; right->wrong 0,0,1,0.
- ALL fresh paired confirmations (gen_18,20,21,22,23,24,25; n=448): original ~1.1%, v2 ~28%; +26.8 pts; 122 wrong->right, 2 right->wrong.
- FINAL SUBMISSION = v2 (edited == best_1 verified: True). All 25 passes used.
