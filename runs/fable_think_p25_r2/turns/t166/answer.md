```python
# Where else does L18n2800 (and other candidate neurons) fire? Check fwd_8 long traces (mlp_down_in_L18..23) and fwd_9
A8_18=np.load(os.path.join(d8,'mlp_down_in_L18.npy'), mmap_mode='r')
def profile(Aarr, idsl, l_n_list, topn=6):
    for (l,n) in l_n_list:
        vals=[]
        for i,ids in enumerate(idsl):
            a=np.asarray(Aarr[i,:len(ids),n]).astype(np.float32)
            for p in range(len(ids)): vals.append((abs(a[p]), a[p], i, p))
        vals.sort(key=lambda x:-x[0])
        print(f'L{l}n{n}: top |act| positions:')
        for v in vals[:topn]:
            i,p=v[2],v[3]; print('   %.3f'%v[1], repr(tok.decode(idsl[i][max(0,p-6):p+1]))[-70:], '->', repr(tok.decode([idsl[i][p+1]]))[:12] if p+1<len(idsl[i]) else '')
        arr=np.concatenate([np.abs(np.asarray(Aarr[i,:len(ids),n]).astype(np.float32)) for i,ids in enumerate(idsl)])
        print('   frac |act|>0.2: %.4f  >0.3: %.4f  n=%d'%((arr>0.2).mean(), (arr>0.3).mean(), len(arr)))
profile(A8_18, ids8, [(18,2800)])
profile(A9[18], ids9, [(18,2800)])
```