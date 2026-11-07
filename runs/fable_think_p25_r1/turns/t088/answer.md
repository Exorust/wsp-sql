```python
# Find decision points in the loop region: bullet starts (token after '*   ') and bullet ends (token after '.'), compare orig vs edited top-1 and copy-token lp
def tokstr(i): return tok.decode([int(i)])
ex = tok.encode("\n    *   The `Student` table has a `city_code` column.\n    *   The").ids
print([tokstr(i) for i in ex])
```