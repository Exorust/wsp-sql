```python
# Hypothesis: record final combined paired results in notes; re-verify edited == best_1 (v2) is what gets submitted.
import os, glob, json, numpy as np
W='/Users/chandu/myproj/wsp-sql/runs/fable_think_p25_r1/work'
same=all(np.array_equal(np.load(f),np.load(W+'/best_1/'+os.path.basename(f))) for f in glob.glob(W+'/edited/*.npy'))
with open(W+'/notes.md','a') as fh:
    fh.write('''- gen_22..25 (both, confirmD0-3, 64 fresh each): orig 2/64,0/64,1/64,0/64; v2 19/64,19/64,21/64,15/64;
  paired +26.6+-5.6, +29.7+-5.8, +31.3+-6.3, +23.4+-5.3; wrong->right 17,19,21,15; right->wrong 0,0,1,0.
- ALL fresh paired confirmations (gen_18,20,21,22,23,24,25; n=448): original ~1.1%%, v2 ~28%%; +26.8 pts; 122 wrong->right, 2 right->wrong.
- FINAL SUBMISSION = v2 (edited == best_1 verified: %s). All 25 passes used.
'''%same)
print('edited==best_1:',same, edited())
```