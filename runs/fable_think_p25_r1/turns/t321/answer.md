```python
# Hypothesis: finalize notes; print id sets for remaining paired passes (gen_12 halves, gen11 set, gen6 set)
with open(f'{W}/notes.md','a') as f:
    f.write("\n## Session 4 final (passes 19-21)\n- gen_19 (edited, confirmB 64 fresh + 3 BIRD-style Hint prompts): 23/64=35.9%; Hint prompts all skip thinking and give SQL (25-56 tokens).\n- gen_20 (both, confirmC fresh): orig 1/64, v2 13/64; paired +18.8 +- 5.4 (13 w->r, 1 r->w).\n- gen_21 (both, confirmB): orig 2/64, v2 22/64; paired +31.3 +- 5.8 (20 w->r, 0 r->w).\n- Combined fresh paired (gen_18,20,21; n=192): +25.5 pts, 50 wrong->right, 1 right->wrong. FINAL = v2 (edited == best_1 == best_final).\n")
g6=[json.loads(l)['id'] for l in open(f'{W}/gen_6_original.jsonl')]
g11ids=json.load(open(f'{W}/gen_sets_v2.json'))['gen11']
print(json.dumps(ids12[64:])); print(json.dumps(g11ids[:64])); print(len(g6), json.dumps(g6))
```