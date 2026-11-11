```python
# Hypothesis: same; import pandas (earlier cell aborted before import)
import pandas as pd
df=pd.DataFrame(stats,columns=['id','period','start','ntok','cls','err'])
print(df[['period','start']].describe())
print('no period',df['period'].isna().sum(),'no start',df['start'].isna().sum())
print(df['cls'].value_counts())
print(df.head(12))
```