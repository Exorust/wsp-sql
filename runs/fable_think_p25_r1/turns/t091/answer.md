```python
# Save a copy of the current probe-B edit, then set up the confirm pool sample for a paired generation
import shutil, random
if not os.path.exists(W+"/probeB"): shutil.copytree(W+"/edited", W+"/probeB")
splits = json.load(open(W+"/splits.json"))
pool = splits['confirm_pool']; print(len(pool), pool[:5])
random.seed(7); random.shuffle(pool)
genA = pool[:40]; genB = pool[40:100]; genC = pool[100:200]
json.dump({'genA':genA,'genB':genB,'genC':genC}, open(W+"/gen_sets.json","w"))
print(json.dumps(genA))
```