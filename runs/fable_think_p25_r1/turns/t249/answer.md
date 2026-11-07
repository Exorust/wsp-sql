```python
# Hypothesis: in the 7 loop texts, find the answer-region where the period repeats; show per-period the copied token lp vs best alternative at the first repetition onset.
def find_period(ids, start, maxp=200):
    # smallest p such that ids[i]==ids[i-p] for the tail
    n=len(ids)
    for p in range(1,maxp):
        if n-start>3*p and all(ids[i]==ids[i-p] for i in range(n-2*p,n)): return p
    return None
loop_info=[]
for k in range(7):
    ids=ids13[k]; txt=texts13[k]
    a=txt.find('</think>'); astart=len(tok.encode(txt[:a]).ids)
    p=find_period(ids,astart)
    # onset: first i>=astart where ids[i:i+p]==ids[i+p:i+2p]
    onset=None
    if p:
        for i in range(astart,len(ids)-2*p):
            if ids[i:i+p]==ids[i+p:i+2*p]: onset=i;break
    loop_info.append((k,astart,p,onset))
    print(k,it13[k]['id'],'len',len(ids),'ans_start',astart,'period',p,'onset',onset, repr(tok.decode(ids[onset:onset+p]))[:80] if onset else '')
```