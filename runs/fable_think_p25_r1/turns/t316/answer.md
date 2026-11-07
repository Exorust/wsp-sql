```python
# Hypothesis: prepare two more fresh 64-id confirmation sets (no code needed later) and back up final edit
import shutil
rest=[x for x in pool if x not in set(conf)]; random.seed(11); s2=random.sample(rest,128)
json.dump({'confirmB':s2[:64],'confirmC':s2[64:]},open(f'{W}/gen_sets_confirm2.json','w'))
if os.path.exists(f'{W}/best_final'): shutil.rmtree(f'{W}/best_final')
shutil.copytree(f'{W}/edited', f'{W}/best_final')
print(json.dumps(s2[:64])); print(json.dumps(s2[64:]))
```