```python
# Identify token ids for fence and keywords at line start; find the sql region start in each text
ids_fence=tok.encode('x\n'+FENCE+'<|im_end|>').ids; print([ (i,tok.decode([i])) for i in ids_fence])
ids_and=tok.encode('x\nAND y').ids; print([ (i,tok.decode([i])) for i in ids_and])
ids_join=tok.encode('x\nJOIN y\nOR z\nWHERE').ids; print([ (i,tok.decode([i])) for i in ids_join])
def find_sql_start(ids):
    for i in range(len(ids)-2):
        if ids[i]==198 and tok.decode(ids[i-2:i+1]).endswith('sql\n') and tok.decode(ids[i-2:i+1]).startswith('`'):
            pass
    # simpler: find '</think>' then the first 198 after 'sql'
    txt_pos=None
    for i in range(len(ids)):
        if tok.decode(ids[max(0,i-3):i+1]).endswith('sql\n') and i>0: return i
    return None
starts=[find_sql_start(e) for e in enc13]; print(starts)
```