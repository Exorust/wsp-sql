```python
# Hypothesis: file mtimes tell when the current edit was saved relative to passes 12-15
import time
def mt(p): return time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p)))
for n in edited(): print(n.split('.')[3], mt(f'{W}/edited/{n}.npy'), 'best_1', mt(f'{W}/best_1/{n}.npy'))
for k in range(10,16): print(k, mt(f'{W}/fwd_{k}.done.json'))
print('notes', mt(f'{W}/notes.md'))
print(os.listdir(f'{W}/edited_model')[:5], os.listdir(f'{W}/v1_backup')[:5])
```