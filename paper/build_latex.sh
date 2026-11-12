#!/usr/bin/env bash
# Build the MDPI-class LaTeX version of the manuscript (requires TeX Live).
set -euo pipefail
cd "$(dirname "$0")"
python3 prep_latex.py
python3 tables_latex.py latex/body.tex
mkdir -p latex/figures
cp ../figures/fig_damad_architecture.png ../figures/fig_gapmap.png ../figures/fig_ablation.png \
   ../figures/fig_drift.png ../figures/fig_shots.png ../figures/fig_trace_smd_sudden.png \
   ../figures/fig_trace_swat_sudden.png latex/figures/
sed '/^@inproceedings{kim2022rigorous/,/^}/{/^\s*number\s*=/d}' references.bib > latex/references.bib
cd latex
pdflatex -interaction=nonstopmode -halt-on-error manuscript_make.tex > build.log 2>&1 || { tail -40 build.log; exit 1; }
bibtex manuscript_make >> build.log 2>&1 || true
pdflatex -interaction=nonstopmode -halt-on-error manuscript_make.tex >> build.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error manuscript_make.tex >> build.log 2>&1
grep -c 'Warning' build.log || true
rm -f ../manuscript_make_latex.zip
zip -q -r ../manuscript_make_latex.zip manuscript_make.tex body.tex references.bib Definitions figures manuscript_make.pdf manuscript_make.bbl
ls -la manuscript_make.pdf ../manuscript_make_latex.zip
