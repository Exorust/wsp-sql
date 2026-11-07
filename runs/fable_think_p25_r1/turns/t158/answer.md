```python
# Gold texts: did v1 change the logprob of the SQL answer tokens? (sum over tokens after </think>)
res=[]
for a in range(8,20):
    o=sel[a]; ids=enc8[a]; T=len(ids)
    jth=ids.index(th_id)
    s4=np.nansum(lp4[o,jth+1:T]); s8=np.nansum(lp8[a,jth+1:T])
    # also p(</think>) after '<think>\n\n' and lp of '\n\n' after <think>
    st=ids.index(tok.encode('<think>').ids[0])
    res.append((a, T-jth-1, round(float(s4),2), round(float(s8),2), round(float(lp4[o,jth]),2), round(float(lp8[a,jth]),2)))
r=pd.DataFrame(res,columns=['text','n_sql_tok','lp_sql_orig','lp_sql_edit','lp_think_end_orig','lp_think_end_edit'])
print(r.to_string()); print('mean per-token sql lp orig %.3f edit %.3f'%((r.lp_sql_orig/r.n_sql_tok).mean(),(r.lp_sql_edit/r.n_sql_tok).mean()))
# per-token worst changes in SQL region
worst=[]
for a in range(8,20):
    o=sel[a]; ids=enc8[a]; T=len(ids); jth=ids.index(th_id)
    for j in range(jth+1,T):
        worst.append((float(lp8[a,j]-lp4[o,j]), a, repr(tok.decode([ids[j]]))))
worst.sort(); print('most hurt tokens:',worst[:6]); print('most helped:',worst[-4:])
```