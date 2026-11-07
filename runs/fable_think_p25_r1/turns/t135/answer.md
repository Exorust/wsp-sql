```python
# Compare key neurons across all in-think '\n\n' positions: next=digit (exit) vs next='   ' (continue)
keyn={23:[580,932,385,380,9],22:[796,1267,223,87],21:[206,52,198],20:[168,669],18:[128,942,259],17:[1726,545],16:[173]}
digit_ids=set(tok.encode(s).ids[0] for s in '0123456789')
rows=[]
for i in range(6):
    ids=enc[i]; st=ids.index(tok.encode('<think>').ids[0])
    for j in [j for j,x in enumerate(ids) if x==271 and j>st and j+1<len(ids)]:
        nxt=ids[j+1]; kind='digit' if nxt in digit_ids else ('indent' if nxt==id_ind else 'other')
        # margin: lp(indent)-lp(top digit) from topk
        row=tk[i,j]; lps=tlp[i,j]
        def lpof(tid):
            w=np.where(row==tid)[0]; return float(lps[w[0]]) if len(w) else -20.
        best_digit=max(lpof(d) for d in digit_ids)
        rows.append(dict(i=i,j=j,kind=kind,margin=lpof(id_ind)-best_digit,
                         **{f'L{L}n{n}':float(neuron_contrib(L,i,j,id_ind,id_3)[n]) for L in keyn for n in keyn[L]}))
import pandas as pd
df=pd.DataFrame(rows); pd.set_option('display.width',250); pd.set_option('display.max_columns',40)
print(df.groupby('kind').size())
print(df.groupby('kind').mean(numeric_only=True).round(2).T)
```