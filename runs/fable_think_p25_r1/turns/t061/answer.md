```python
# Save notes with recovered state and the lesson about the forward block (no file refs; JSON must be inline)
notes = """# Notes

## State
- 3/25 forward passes used (pass 3 WASTED: "texts": "@@FILE" is not allowed; JSON must be inline in the forward block; kernel output cut at 10k chars so print in chunks).
- Code cannot contain triple backticks (block ends); use FENCE = "`"*3.

## Findings
- gen_1 (original, 128 diag problems, 8192 tok): accuracy 1.6%, 99% cut at max tokens, 95% visibly looping. Only 1/128 reached </think>.
  The model writes "Thinking Process: 1. Analyze the Request ... 2. Analyze the Schema ..." then loops on bullets like
  "*   The `Dorm` table has `gender`." or "*   Does the `entrepreneur` table have `X`? Yes." forever.
- fwd_2 (teacher-forced, 2 loop texts, attention at 3,7,11,15,19,23): in the loop region, induction heads (mass on t+1-period):
  L15h7 0.26 (+0.17 on 2 periods back), L11h1 0.10, L23h5 0.12, L19h5 0.08, L23h7 0.08, L23h4 0.07, L23h0 0.06. L23h2 is a self-attention head (0.58).
- Loop is SOFT: at bullet start (after "*  ") p(' The')~0.35-0.58 vs ' So' ~0.12, ' Wait' ~0.05-0.13; after bullet end, p('\\n\\n')~0.1-0.25 (would start a new section).
  Margin ~1-1.5 nats. Greedy always picks the copy token.

## Files
- splits.json: diag (128 ids used in gen_1), confirm_pool (2000 ids unused).
- setA.json: 119 loop texts (raw rendered, thinking inside <think>, truncated after a few periods) with 'onset','period' in tokens.
- setB.json: 200 gold-SQL texts rendered with empty thinking.
- req3.json: the 319-text request (too big to paste inline; 1MB).

## Edits tried
(none yet)
"""
open(W+"/notes.md","w").write(notes)
# Build a compact teacher-forced request: shortest loop texts + shortest gold texts
la = sorted(setA, key=lambda x: len(x['text']))
lb = sorted(setB, key=lambda x: len(x['text']))
print([len(x['text']) for x in la[:25]])
print([len(x['text']) for x in lb[:40]])
```