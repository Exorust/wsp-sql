#!/bin/bash
# Builds every figure to PDF (for main.tex) and PNG (for the blog). TikZ figures compile alone with tectonic; f2 is mermaid.
cd "$(dirname "$0")"
for f in f1_setup f3_mechanism f4_outcomes f5_continuation f6_pigeon; do
  printf '\\documentclass[border=4pt]{standalone}\\usepackage[T1]{fontenc}\\usepackage{lmodern,tikz,amsmath}\\newcommand{\\think}{\\texttt{</think>}}\\begin{document}\\input{%s_body}\\end{document}\n' $f > $f.wrap.tex
  cp $f.tex ${f}_body.tex && tectonic -o . $f.wrap.tex 2>&1 | grep -iE "^error|! " ; mv $f.wrap.pdf $f.pdf; rm -f $f.wrap.tex ${f}_body.tex
done
MMDC=$(ls ~/.npm/_npx/*/node_modules/.bin/mmdc | head -1)
$MMDC -i f2_session.mmd -o f2_session.pdf -q
for f in f1_setup f2_session f3_mechanism f4_outcomes f5_continuation f6_pigeon; do pdftoppm -png -r 200 -singlefile $f.pdf $f; done
