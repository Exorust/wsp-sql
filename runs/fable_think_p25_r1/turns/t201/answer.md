```python
# Detector activations at first position per text vs prompt length (tokens)
plen = [first_pos[n] for n in range(6)]
print("prompt lengths:", plen)
for (l,j) in [(17,537),(18,628),(19,2424),(20,1235)]:
    print((l,j), [round(float(Mall[l][n,first_pos[n],j]),2) for n in range(6)])
# Also: in gen_1_acts (original, 128 problems) is there the residual at the last prompt token? check index.json
print(os.listdir(f"{W}/gen_1_acts")); print(open(f"{W}/gen_1_acts/index.json").read()[:600])
```