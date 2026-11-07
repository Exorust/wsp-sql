```python
# Hypothesis: texts 0-2 have longer/irregular periods; inspect tails and detect period with a looser criterion (match of last 2 periods allowing up to 400).
for k in range(3):
    ids=ids13[k]; print(k, repr(tok.decode(ids[-160:]))[:400])
```