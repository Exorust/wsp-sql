```python
# For fwd_2 text0: per-head attention mass on prompt (schema) during schema-listing region vs mass on previous period during loop
ids = ids0; T=1340
# find schema listing region: from '2.  **Analyze the Schema' to '3.'
txt_pos = []
dec = [tok.decode(ids[:t+1]) for t in range(T)]  # cumulative decode (slow but fine)
def pos_of(sub, start_char=0):
    full = dec[-1]; c = full.find(sub, start_char)
    if c<0: return None
    for t in range(T):
        if len(dec[t])>c: return t
s2 = pos_of("2.  **Analyze the Schema"); s3 = pos_of("3.  **", 0); 
print("schema section tokens", s2, s3, "prompt end", 245, "loop onset", onset0)
qs = np.arange(s2+8, s3)   # positions in schema listing
rows_out=[]
for L in layers_fa:
    a = A[L].astype(np.float32)
    for h in range(8):
        m_s = a[h][qs]; m_l = a[h][np.arange(onset0+p0, T-1)]
        rows_out.append((L,h, m_s[:, :245].sum(1).mean(), m_s[:, 245:].sum(1).mean()-np.array([m_s[i,q] for i,q in enumerate(qs)]).mean(),
                         m_l[:, :245].sum(1).mean(), np.array([m_l[i,q+1-p0]+m_l[i,q+1-2*p0] for i,q in enumerate(np.arange(onset0+p0,T-1))]).mean()))
dfh = pd.DataFrame(rows_out, columns=['L','h','schema_sec:prompt','schema_sec:own_text','loop:prompt','loop:induct'])
print(dfh.round(3).to_string())
```