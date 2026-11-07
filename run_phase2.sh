#!/bin/bash
# Phase 2, validity controls for one editor run, all on BIRD Mini-Dev with thinking on (150 evenly spaced questions, same as Phase 0).
# One GPU job at a time; runs with summary.json are skipped, so the script can be rerun after an interruption.
# usage: ./run_phase2.sh runs/fable_think_p25_r1
cd "$(dirname "$0")"; PY=.venv/bin/python; RUN=$1; tag=$(basename $RUN)
EDITED=$RUN/work/edited_model; [ -d "$EDITED" ] || { echo "no edited model at $EDITED"; exit 1; }
ev() { local out=$1; shift; [ -f $out/summary.json ] || $PY eval_sql.py --bench bird --thinking 1 --max-tokens 8192 --batch 8 --n 150 --out $out "$@" 2>&1 | grep --line-buffered -v Warning; }
ev runs/p2_${tag}_think --model $EDITED                                                   # the editor's edit (base: runs/p0_base_think)
[ -f runs/p2_base_nothink8192/summary.json ] || $PY eval_sql.py --model models/Qwen3.5-0.8B --bench bird --thinking 0 --max-tokens 8192 --batch 8 --n 150 --out runs/p2_base_nothink8192 2>&1 | grep --line-buffered -v Warning   # template-flag control: what skipping thinking is worth
[ -d runs/ctrl_random_${tag} ] || $PY control_random.py --footprint $EDITED --draws 5 --out runs/ctrl_random_${tag} 2>&1 | grep -v Warning
for k in 0 1 2 3 4; do ev runs/p2_ctrl_random_${tag}_$k --model runs/ctrl_random_${tag}/draw_$k/edited_model --n 50; done   # random location, same footprint; 50 q each because they loop
if [ ! -d runs/sft_${tag}/edited_model ]; then
  PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.6 PYTORCH_MPS_LOW_WATERMARK_RATIO=0.5 $PY baseline_sft.py --footprint $EDITED --thinking 1 --n 500 --steps 250 --batch 2 --out runs/sft_${tag} 2>&1 | grep -v Warning
fi
ev runs/p2_sft_${tag}_think --model runs/sft_${tag}/edited_model                                   # gradient descent on the same 4,083 entries
echo PHASE2_DONE
