```python
# (fix) decision_points takes index
def decision_points(j):
    enc=tok.encode(T[j]); offs=enc.offsets; toks=[T[j][x:y] for x,y in offs]; a0,b0,_=my_sql_span(T[j])
    out={}
    for p in range(a0,b0):
        if toks[p].strip().upper()=='SELECT': out['SEL']=p; break
    for p in range(a0,b0):
        if toks[p].strip().upper()=='FROM':
            q=p+2
            while q<b0 and not toks[q].startswith(' '): q+=1
            if q<b0: out['FROM']=q-1
            break
    return out,toks
rows=[]
for j in range(32):
    dp,toks=decision_points(j); dp1,toks1=decision_points(32+j)
    r={}
    for key in dp:
        if key not in dp1: continue
        p0,p1=dp[key],dp1[key]
        d0=dict(zip(tk_ids[j,p0].tolist(),tk_lp[j,p0].tolist())); d1=dict(zip(tk_ids[32+j,p1].tolist(),tk_lp[32+j,p1].tolist()))
        if key=='SEL':
            r['dist0']=d0.get(57088,-15); r['dist1']=d1.get(57088,-15)
            r['gold0']=float(lp[j,p0+1]); r['gold1']=float(lp[32+j,p1+1])
            r['top0']=tok.decode([int(tk_ids[j,p0][0])]); r['top1']=tok.decode([int(tk_ids[32+j,p1][0])])
        else:
            r['fgold0']=float(lp[j,p0+1]); r['fgold1']=float(lp[32+j,p1+1]); r['ftop0']=tok.decode([int(tk_ids[j,p0][0])]); r['ftop1']=tok.decode([int(tk_ids[32+j,p1][0])])
    rows.append(r)
import pandas as pd
df=pd.DataFrame(rows); print(df[['dist0','dist1','gold0','gold1','fgold0','fgold1']].mean().round(2))
print('DISTINCT top1 plain/I1:', sum(df.top0.str.strip()=='DISTINCT'), sum(df.top1.str.strip()=='DISTINCT'))
print('alias-letter top1 after SELECT plain/I1:', sum(df.top0.str.strip().str.len()<=2), sum(df.top1.str.strip().str.len()<=2))
print(df[['top0','top1','ftop0','ftop1']].to_string())
```