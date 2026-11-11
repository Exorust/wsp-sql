```python
# Check for massive activation channels in h24 and their norm weights
h24=H[24][0,p].astype(np.float32); a=np.abs(h24); top=np.argsort(-a)[:8]
print('top dims', top, 'vals', np.round(h24[top],1), '(1+w)', np.round((1+wn.numpy())[top],3))
print('share of sq norm in top 4 dims:', round(float((a[top[:4]]**2).sum()/(a**2).sum()),3))
att=H[24][0,p].astype(np.float32)-H[23][0,p].astype(np.float32)-Wd23@M23[0,p].astype(np.float32)
print('attn out top dims', np.argsort(-np.abs(att))[:6], np.round(att[np.argsort(-np.abs(att))[:6]],1))
# Also check at a mid-text position
q=300; h=H[24][0,q].astype(np.float32); print('mid pos norms h23,h24:', round(float(np.linalg.norm(H[23][0,q].astype(np.float32))),1), round(float(np.linalg.norm(h)),1), 'top dims', np.argsort(-np.abs(h))[:4])
```