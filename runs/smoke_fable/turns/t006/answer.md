```python
# Decision first: the paired test of the L23h2 knock-out gave -2.0 +/- 2.1 points (11 wrong->right, 16 right->wrong; looping 3.1%->4.7%, no_such_column 69->70), so the hypothesis "this suppressor causes invented columns" is NOT supported -> drop the edit before anything else, then read the generations to document how the model actually fails.
import re, shutil
for nme in list(edited()): print('drop:',drop_edit(nme))
print('edited now:',edited(),'| edited dir:',os.listdir(W+'/edited') if os.path.isdir(W+'/edited') else 'absent')
open(W+'/notes.md','a').write("""
## PAIRED PASS (the only forward pass), 248 practice problems + 8 own prompts, original vs L23h2 knock-out
- original acc 30.65%, edited 28.63%; paired diff -2.02 +/- 2.10 pts; wrong->right 11, right->wrong 16.
- looping 3.1% -> 4.7%, cut at max tokens 3.9% -> 6.25%, mean tokens 89.6 -> 112.5; no_such_column 69 -> 70 (unchanged), wrong_result 85 -> 90.
- Conclusion: prediction (fewer invented columns) refuted; side effect (more repetition) observed. EDIT DROPPED. Final submission = no edits (unedited weights).
""")
try:
    O=[json.loads(l) for l in open(W+'/gen_1_original.jsonl')]; Ed=[json.loads(l) for l in open(W+'/gen_1_edited.jsonl')]
    print(len(O),len(Ed)); print({k:str(v)[:90] for k,v in O[0].items()}); print('last rec keys',{k:str(v)[:60] for k,v in O[-1].items()})
    def pick(r,c):
        for k in c:
            if k in r: return k
    kid=pick(O[0],['id','problem','problem_id','pid','item']); ktext=pick(O[0],['text','output','answer','completion','response']); ksql=pick(O[0],['sql','extracted_sql','pred_sql','query']); kgr=pick(O[0],['grade','class','failure','status','result','correct']); kerr=pick(O[0],['error','sqlite_error','message','err'])
    print('fields',kid,ktext,ksql,kgr,kerr)
    P2={p['id']:p for p in probs}
    def loopy(t):
        t=t or ''
        return len(t)>=400 and any(t.count(t[-L:])>=6 for L in (10,20,40))
    eo={r.get(kid):r for r in O}; ee={r.get(kid):r for r in Ed}
    ids=[r.get(kid) for r in O if r.get(kid) in P2]; print('graded items',len(ids),'others',len(O)-len(ids))
    xt=collections.Counter((str(eo[i].get(kgr)),str(ee[i].get(kgr))) for i in ids)
    print('grade cross-tab (orig -> edited):',sorted(xt.items(),key=lambda x:-x[1])[:14])
    same=sum((eo[i].get(ksql) or '').strip()==(ee[i].get(ksql) or '').strip() for i in ids); print('identical extracted SQL orig vs edited: %d/%d'%(same,len(ids)))
    lo={i:loopy(eo[i].get(ktext)) for i in ids}; le={i:loopy(ee[i].get(ktext)) for i in ids}
    print('my loop detector: orig',sum(lo.values()),'edited',sum(le.values()),'both',sum(lo[i] and le[i] for i in ids),'new in edited',[i for i in ids if le[i] and not lo[i]][:8],'cured',[i for i in ids if lo[i] and not le[i]][:8])
    lens=[len(tok.encode(eo[i].get(ktext) or '').ids) for i in ids]
    print('orig answer tokens pct 50/90/99',np.percentile(lens,[50,90,99]),'| slen of looping dbs',[slen[P2[i]['db']] for i in ids if lo[i]])
    for i in [i for i in ids if lo[i]][:4]: print(' LOOP orig',i,'|',(eo[i].get(ktext) or '')[-170:].replace('\n',' '))
    for i in [i for i in ids if le[i] and not lo[i]][:3]: print(' LOOP new ',i,'|',(ee[i].get(ktext) or '')[-170:].replace('\n',' '))
    # no_such_column: invented name vs a real column used on the wrong table/alias
    inv=ex=0; shown=0
    for i in ids:
        r=eo[i]; msg=str(r.get(kerr) or '')
        m=re.search(r'no such column: ?([^\s,;]+)',msg)
        if not m: continue
        col=m.group(1).split('.')[-1].strip('"`[]').lower(); sch=schemas[P2[i]['db']].lower()
        isin=re.search(r'(?<![a-z0-9_])'+re.escape(col)+r'(?![a-z0-9_])',sch) is not None
        ex+=isin; inv+=(not isin)
        if shown<6: shown+=1; print(' NSC',i,'in_schema' if isin else 'INVENTED',msg[:60],'| pred:',(r.get(ksql) or '')[:110].replace('\n',' '),'| gold:',P2[i]['gold'][:90])
    print('no_such_column in original: column name exists somewhere in schema (wrong table/alias):',ex,'| name not in schema at all (invented):',inv)
    acc_by=collections.defaultdict(list)
    for i in ids: acc_by[min(3,slen[P2[i]['db']]//300)].append(str(eo[i].get(kgr)))
    print('orig grade by schema length bucket (x300 tok):',{b:(len(v),collections.Counter(v).most_common(3)) for b,v in sorted(acc_by.items())})
    for r,r2 in list(zip(O,Ed))[-8:]:
        if r.get(kid) in P2: continue
        print(' OWN prompt | orig:',(r.get(ksql) or r.get(ktext) or '')[:150].replace('\n',' '),'| loop o/e',loopy(r.get(ktext)),loopy(r2.get(ktext)))
except Exception as e:
    import traceback; print('analysis err',traceback.format_exc()[-800:])
```