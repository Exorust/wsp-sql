```python
# Hypothesis: see the schema text format the model sees; then choose a stratified diagnostic sample
db0=df.db.iloc[0]
print(schemas[db0][:700])
# stratified sample: 128 problems from distinct dbs, mixed gold complexity
random.seed(0)
df['gold_len']=df.gold.str.len()
df['has_join']=df.gold.str.upper().str.contains('JOIN')
df['has_group']=df.gold.str.upper().str.contains('GROUP BY')
df['has_sub']=df.gold.str.upper().str.count('SELECT')>1
print(df[['has_join','has_group','has_sub']].mean())
# pick: one per db for the first 128 dbs ordered randomly (so dbs don't repeat)
dbs=list(df.db.unique()); random.shuffle(dbs)
diag=[]
for db in dbs[:128]:
    sub=df[df.db==db]
    diag.append(sub.sample(1,random_state=1).iloc[0])
diag=pd.DataFrame(diag)
print(diag[['has_join','has_group','has_sub']].mean(), len(diag))
diag_ids=diag.id.tolist()
rest_dbs=dbs[128:]
print(diag_ids[:10])
```