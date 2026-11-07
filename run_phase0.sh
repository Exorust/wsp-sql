#!/bin/bash
# Phase 0: 4 runs, sequential (one model in memory at a time). Finished runs (summary.json present) are skipped.
# Thinking runs use 150 evenly spaced questions: the full 500 would take 2 to 4.5 hours on the laptop.
cd "$(dirname "$0")"
PY=.venv/bin/python
for m in Qwen3.5-0.8B Qwen3.5-0.8B-weight-space-programming; do
  tag=$([ "$m" = Qwen3.5-0.8B ] && echo base || echo mathedit)
  [ -f runs/p0_${tag}_nothink/summary.json ] || $PY eval_sql.py --model models/$m --bench bird --thinking 0 --max-tokens 1024 --batch 16 --out runs/p0_${tag}_nothink 2>&1 | grep --line-buffered -v Warning
  [ -f runs/p0_${tag}_think/summary.json ] || $PY eval_sql.py --model models/$m --bench bird --thinking 1 --max-tokens 8192 --batch 8 --n 150 --out runs/p0_${tag}_think 2>&1 | grep --line-buffered -v Warning
done
echo PHASE0_DONE
