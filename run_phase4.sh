#!/bin/bash
# Phase 4, short runs after the adversarial review. One GPU job at a time. Every run saves a checkpoint after each batch
# (runs/<name>/partial.jsonl), a finished run (summary.json) is skipped, and a failed run is tried 3 times, so the script
# can be stopped, or the laptop can sleep, and `./run_phase4.sh` continues where it was.
cd "$(dirname "$0")"
BASE=models/Qwen3.5-0.8B; ME=models/Qwen3.5-0.8B-weight-space-programming
R1=runs/fable_think_p25_r1/work/edited_model; R2=runs/fable_think_p25_r2/work/edited_model
S="--temp 0.6 --top-p 0.95 --top-k 20 --presence 1.5"      # report, thinking on
C="--temp 0.7 --top-p 0.8 --top-k 20 --presence 1.5"       # model card, thinking off
B="--bench bird --n 150 --max-tokens 8192"
ev() { for try in 1 2 3; do [ -f runs/$1/summary.json ] && return; echo "== $1 (try $try) $(date +%H:%M)"
       .venv/bin/python eval_sql.py --out runs/$1 --batch 8 "${@:2}" | grep -v '^ *"\|^[{}]'; done; echo "FAILED $1"; }
# C. closing tag forced by the template, on edited weights: what the bypass edits do to the SQL after thinking closes
ev p4_tagoff_r1_greedy --model $R1 $B --thinking 0
ev p4_tagoff_r2_greedy --model $R2 $B --thinking 0
ev p4_tagoff_r1_samp   --model $R1 $B --thinking 0 $C
ev p4_tagoff_r2_samp   --model $R2 $B --thinking 0 $C
# B. the same looping prefixes (from the sampled base run) continued by each model
P="$B --thinking 1 --prefix-from runs/p3_bird_base_samp/results.jsonl --prefix-n 60 --max-tokens 4096 --batch 4 $S"
ev p4_prefix_base     --model $BASE $P
ev p4_prefix_mathedit --model $ME   $P
ev p4_prefix_r1       --model $R1   $P
ev p4_prefix_r2       --model $R2   $P
# A. the math edit's change vectors moved to random neurons, under sampling (the control the Fable edits already had)
[ -d runs/p4_ctrl_random_mathedit/draw_2/edited_model ] || .venv/bin/python control_random.py --footprint $ME --draws 3 --out runs/p4_ctrl_random_mathedit
for k in 0 1 2; do ev p4_ctrl_random_mathedit_$k --model runs/p4_ctrl_random_mathedit/draw_$k/edited_model --bench bird --n 50 --max-tokens 8192 --thinking 1 $S; done
# D. two more sampling seeds for the five SQL rows of phase 3
for s in 1 2; do
ev p4_bird_mathedit_samp_s$s --model $ME   $B --thinking 1 $S --seed $s
ev p4_bird_base_samp_s$s     --model $BASE $B --thinking 1 $S --seed $s
ev p4_bird_nothink_samp_s$s  --model $BASE $B --thinking 0 $C --seed $s
ev p4_bird_r1_samp_s$s       --model $R1   $B --thinking 1 $S --seed $s
ev p4_bird_r2_samp_s$s       --model $R2   $B --thinking 1 $S --seed $s
done
# F. unedited model and math edit on the same 50 questions as the random-location control
ev p4_ctrl50_base     --model $BASE --bench bird --n 50 --max-tokens 8192 --thinking 1 $S
ev p4_ctrl50_mathedit --model $ME   --bench bird --n 50 --max-tokens 8192 --thinking 1 $S
echo PHASE4_DONE
