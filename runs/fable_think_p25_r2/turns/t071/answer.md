```python
# Does the 3-head ablation hurt SQL-writing? Compare gold-SQL token logprobs orig vs edited on the 16 gold chats (texts 6..21)
def ans_start(text):
    # token index where '</think>' ends
    pre=text.split('</think>')[0]+'</think>'
    return len(tok.encode(pre).ids)
tot3=[];tot4=[]
for i in range(6,22):
    a=ans_start(texts[i]); n=m3['lengths'][i]
    s3=np.nanmean(lp3[i,a:n]); s4=np.nanmean(lp4[i,a:n]); tot3.append(s3); tot4.append(s4)
print('gold SQL mean lp orig %.3f edit %.3f'%(np.mean(tot3),np.mean(tot4)))
print(np.round(np.array(tot4)-np.array(tot3),3))
# also the "</think>" token itself when thinking is empty
```