```python
# Retry printing (no literal triple backticks): shortest 12 base texts, JSON-escaped with backticks as \u0060
BT='`'*3
order=np.argsort([len(T[i]) for i in range(32)])[:12]; sel=[int(i) for i in order]
json.dump({'sel':sel,'INSTR2':INSTR2,'INSTR3':INSTR3,'INSTR4':INSTR4},open(os.path.join(W,'tf21_plan.json'),'w'))
print(sel, sum(len(T[i]) for i in sel))
for i in sel: print(json.dumps(T[i]).replace(BT,'\\u0060\\u0060\\u0060'))
```