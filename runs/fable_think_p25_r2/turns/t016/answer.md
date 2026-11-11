```python
# Hypothesis: loops start early in thinking; measure where repetition begins and the loop period for each text
import re
def loop_info(text, minlen=40):
    # find earliest index i such that text[i:i+minlen] occurs again later and from there a periodic pattern dominates the tail
    tail=text[-3000:]
    # period estimate: smallest p such that tail[p:] == tail[:-p] mostly
    best=None
    for p in range(20,1500):
        a=tail[p:]; b=tail[:-p]
        match=sum(1 for x,y in zip(a,b) if x==y)/len(a)
        if match>0.95: best=p; break
    # loop start: earliest i where text[i:i+200] appears again
    start=None
    for i in range(0,len(text)-400,50):
        seg=text[i:i+200]
        j=text.find(seg,i+100)
        if j!=-1: start=i; break
    return best,start
stats=[]
for r in rows:
    p,s=loop_info(r['text'])
    stats.append((r['id'],p,s,r['n_tokens'],r['cls'],r['err'][:40] if r['err'] else None))
import pandas as pd
df=pd.DataFrame(stats,columns=['id','period','start','ntok','cls','err'])
print(df.describe())
print(df['period'].isna().sum(), df['start'].isna().sum())
print(df.head(20))
```