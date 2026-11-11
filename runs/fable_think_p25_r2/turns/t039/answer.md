```python
# Hypothesis: heads driving the loop put much mass on earlier copies of the NEXT token (any period); compute copy scores per head in loop vs pre-loop
def copy_scores(ti, ids, start, pl):
    T=len(ids); arr=np.array(ids)
    out={}
    for l in L:
        A=np.load(F+f'/attn_L{l}_text{ti}.npy')
        H=A.shape[0]
        res=np.zeros((H,4))  # ind_loop, ind_pre, dup_loop, dup_pre
        for region,(a,b),col in [('loop',(start+5,T-1),0),('pre',(pl+5,start-1),1)]:
            indm=[];dupm=[]
            for t in range(a,b):
                nxt=arr[t+1]; cur=arr[t]
                m_ind=(arr[:t]==nxt)  # positions j<t with token == next token
                m_dup=(arr[:t]==cur)
                indm.append(A[:,t,:t][:,m_ind].sum(1)); dupm.append(A[:,t,:t][:,m_dup].sum(1))
            res[:,col]=np.mean(indm,0); res[:,2+col]=np.mean(dupm,0)
        out[l]=res
    return out
C0=copy_scores(0, ids0, 604, 155); C1=copy_scores(1, ids1, 1016, 440)
for l in L:
    print('L',l,'  ind loop/pre  text0:',C0[l][:,0],'/',C0[l][:,1])
    print('        ind loop/pre  text1:',C1[l][:,0],'/',C1[l][:,1])
    print('        dup loop text0:',C0[l][:,2],' text1:',C1[l][:,2])
```