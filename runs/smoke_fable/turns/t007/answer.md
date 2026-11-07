**Final submission: the unedited model.** The one edit I could test did not help, so I dropped it; the edited folder is empty (checked after the drop).

**What I tested.** With a single forward pass I could not both diagnose and validate, so I picked one hypothesis from weight analysis alone and spent the pass on a paired comparison.

- **Candidate component:** head 2 of layer 23, the last full-attention layer. Its query/key circuit matches a token to earlier copies of the same token (top-1 for 90.5% of 5,422 schema/SQL tokens, about +1.35 nats at any distance). Its output circuit pushes that token's own logit down (ranked last for essentially every token, z −5.0).
- **Hypothesis:** this head suppresses tokens already present in the prompt, so it might push the model away from schema names and toward invented columns.
- **Edit:** knock the head out by zeroing its 256-column block of `layers.23.self_attn.o_proj.weight`.
- **Prediction:** fewer `no_such_column` errors, with a risk of more repetition.

**Result** (248 practice problems, same items for both models):

| | original | head knocked out |
|---|---|---|
| accuracy | 30.65% | 28.63% |
| `no_such_column` | 69 | 70 |
| `wrong_result` | 85 | 90 |
| looping | 3.1% | 4.7% |
| cut at 1,024 tokens | 3.9% | 6.25% |
| mean answer tokens | 89.6 | 112.5 |

The paired difference is −2.0 ± 2.1 points (11 wrong→right, 16 right→wrong). The prediction failed: invented-column errors did not move. The side effect did appear: by my own loop detector, 11 answers started looping and 4 stopped. The knock-out changed the extracted SQL in 199 of 248 answers, so the head matters broadly, but not in the way I hypothesised. The accuracy drop is about one standard error, so I cannot say the knock-out is harmful either, only that it is not a gain.

**How the original model fails on practice problems.**
- **Wrong column references** are the largest fixable class: 69 of 248. In 53 of them the column exists in the schema but is used on the wrong table or alias; only 16 are names absent from the schema. So the main problem is binding columns to tables, not inventing names.
- **Wrong results** account for 85.
- **Loops** are about 3%: repeated `AND x != NULL` conditions, repeated list values, nested `IN (SELECT ...)`, and runs of whitespace.
- **On my 8 BIRD-style prompts** there were no `CAST(CAST(` loops. The model did write column names containing spaces without quoting (`c.Clinic Name`) and copied the hint's `DIVIDE(...)` pseudo-function literally.

**Not done.** The loop increase suggests this head acts as a repetition brake, so strengthening it is the natural next hypothesis. I had no pass left to test it and did not ship it unmeasured. The saved activations from both runs are unanalysed.

Since no weights changed, the edited model will score the same as the original on the held-out benchmarks.