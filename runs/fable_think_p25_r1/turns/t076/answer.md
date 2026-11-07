```python
# Analyze fwd_4 baseline: loop decision-point margins and gold SQL logprobs
F4 = W+"/fwd_4/"
lp4 = np.load(F4+"token_logprobs.npy"); tk4 = np.load(F4+"topk_ids.npy"); tklp4 = np.load(F4+"topk_logprobs.npy")
items4 = json.load(open(W+"/req4_items.json"))
loop_ids = [tok.encode(x['text']).ids for x in items4['loop']]
gold_ids = [tok.encode(x['text']).ids for x in items4['gold']]
NL = len(loop_ids)
# decision points: positions t (predicting token t+1) in loop region where token t is the bullet marker '*' followed by spaces, i.e. ids[t+1] is the first word of a bullet
def bullet_first_positions(ids, onset):
    pos = []
    for t in range(onset, len(ids)-1):
        s = tok.decode(ids[t-2:t+1])
        if s.endswith("*  ") or s.endswith("*   "):
            # t is the position of the whitespace token after '*'; prediction at t is the first word
            if tok.decode([ids[t]]).strip()=="" and tok.decode([ids[t-1]]).strip()=="*":
                pos.append(t)
    return pos
def bullet_end_positions(ids, onset):
    # positions t where ids[t+1] is a newline token following a bullet (prediction of '\n' vs '\n\n')
    pos = []
    for t in range(onset, len(ids)-1):
        if tok.decode([ids[t+1]]).startswith("\n") and not tok.decode([ids[t]]).startswith("\n"):
            pos.append(t)
    return pos
summary = []
for i,(x,ids) in enumerate(zip(items4['loop'], loop_ids)):
    on, p = x['onset'], x['period']
    bf = bullet_first_positions(ids, on); be = bullet_end_positions(ids, on)
    for t in bf:
        actual = ids[t+1]; lp_act = lp4[i,t+1]
        # best alternative among topk that is not the actual
        alts = [(int(a),float(l)) for a,l in zip(tk4[i,t],tklp4[i,t]) if int(a)!=actual]
        summary.append((x['id'],'first',t,tok.decode([actual]), float(lp_act), tok.decode([alts[0][0]]), alts[0][1]))
    for t in be:
        actual = ids[t+1]; lp_act = lp4[i,t+1]
        alts = [(int(a),float(l)) for a,l in zip(tk4[i,t],tklp4[i,t]) if int(a)!=actual]
        summary.append((x['id'],'end',t,tok.decode([actual]), float(lp_act), tok.decode([alts[0][0]]), alts[0][1]))
dfs = pd.DataFrame(summary, columns=['id','kind','t','actual','lp_actual','alt','lp_alt'])
dfs['margin'] = dfs.lp_actual - dfs.lp_alt
print(dfs.groupby('kind')[['lp_actual','lp_alt','margin']].describe().round(2).T)
print(dfs[dfs.kind=='first'].alt.value_counts().head(8))
print(dfs[dfs.kind=='end'].alt.value_counts().head(5))
```