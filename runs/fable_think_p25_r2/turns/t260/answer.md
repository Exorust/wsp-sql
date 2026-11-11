```python
# debug: compare token counts and find SQL span via offsets instead
enc=tok.encode(T[0]); print(len(enc.ids), L[0]); offs=enc.offsets
s=T[0].index(BT+'sql\n',T[0].index('<|im_start|>assistant'))+7; e=T[0].index(BT,s)
print(s,e, [i for i,(a,b) in enumerate(offs) if b>s][:1], [i for i,(a,b) in enumerate(offs) if a>=e][:1])
```