Fresh start, no prior edits. Let me look at the practice data.

```python
# Hypothesis: practice set structure; check sizes and schema lengths to plan a diagnostic generation pass
import pandas as pd, numpy as np, random
P='/Users/chandu/myproj/wsp-sql/practice'
rows=[json.loads(l) for l in open(P+'/spider_train.jsonl')]
df=pd.DataFrame(rows)
print(df.shape, df.db.nunique())
print(df.head(3).to_dict('records'))
schemas={db:open(f'{P}/schemas/{db}.sql').read() for db in df.db.unique()}
slen={db:len(tok.encode(s).ids) for db,s in schemas.items()}
print(pd.Series(slen).describe())
print(schemas['concert_singer'][:800])
```