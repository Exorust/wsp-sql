```python
# Paired comparison gen_16 (L18+L16) vs gen_17 (L18 only) on overlapping ids
rows17=[json.loads(l) for l in open(os.path.join(W,'gen_17.jsonl'))]
r16={r['id']:r for r in rows}; r17={r['id']:r for r in rows17}
common=[i for i in r17 if i in r16]; print('n17',len(r17),'common',len(common))
c16=np.array([r16[i]['cls']=='correct' for i in common]); c17=np.array([r17[i]['cls']=='correct' for i in common])
d=c16.astype(float)-c17
print('acc L18+L16',c16.mean().round(3),'acc L18 only',c17.mean().round(3),'diff',d.mean().round(3),'se',(d.std()/np.sqrt(len(d))).round(3),'wrong->right',int((c16&~c17).sum()),'right->wrong',int((~c16&c17).sum()))
print('cut: with L16',np.mean([r16[i]['cut'] for i in common]).round(3),'without',np.mean([r17[i]['cut'] for i in common]).round(3))
print('cls with L16',Counter(r16[i]['cls'] for i in common)); print('cls without',Counter(r17[i]['cls'] for i in common))
```