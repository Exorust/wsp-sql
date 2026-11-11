#!/bin/bash
# Phase 3: (a) BIRD rows again under the report's sampling protocol, (b) the three edits on MATH-500.
# One GPU job at a time; a run with summary.json is skipped, so the script can be restarted.
cd "$(dirname "$0")"
BASE=models/Qwen3.5-0.8B; ME=models/Qwen3.5-0.8B-weight-space-programming
R1=runs/fable_think_p25_r1/work/edited_model; R2=runs/fable_think_p25_r2/work/edited_model
S="--temp 0.6 --top-p 0.95 --top-k 20 --presence 1.5"      # report, thinking on
C="--temp 0.7 --top-p 0.8 --top-k 20 --presence 1.5"       # model card, thinking off
ev() { [ -f runs/$1/summary.json ] && return; echo "== $1"; .venv/bin/python eval_sql.py --out runs/$1 --batch 8 "${@:2}" | grep -v '^ *"\|^[{}]'; }
ev p3_bird_r1_samp      --model $R1   --bench bird --n 150 --thinking 1 --max-tokens 8192 $S
ev p3_bird_r2_samp      --model $R2   --bench bird --n 150 --thinking 1 --max-tokens 8192 $S
ev p3_bird_nothink_samp --model $BASE --bench bird --n 150 --thinking 0 --max-tokens 8192 $C
ev p3_bird_mathedit_samp --model $ME  --bench bird --n 150 --thinking 1 --max-tokens 8192 $S
ev p3_bird_base_samp    --model $BASE --bench bird --n 150 --thinking 1 --max-tokens 8192 $S
ev p3_math_r1           --model $R1   --bench math --n 100 --thinking 1 --max-tokens 16384 $S
ev p3_math_r2           --model $R2   --bench math --n 100 --thinking 1 --max-tokens 16384 $S
ev p3_math_nothink      --model $BASE --bench math --n 100 --thinking 0 --max-tokens 8192 $C
ev p3_math_mathedit     --model $ME   --bench math --n 100 --thinking 1 --max-tokens 16384 $S
ev p3_math_base         --model $BASE --bench math --n 100 --thinking 1 --max-tokens 16384 $S
echo PHASE3_DONE
