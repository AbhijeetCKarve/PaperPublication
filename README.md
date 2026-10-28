# Journal submissions: meta-learning anomaly detection on industrial IoT streams

This repository holds the two manuscripts prepared for Q2 journal submission,
the code that produced every number in them, and the systematic review that
backs the first paper.

| Folder | Contents |
|---|---|
| `paper/` | Paper 1: *Drift-aware meta-adaptive anomaly detection for few-shot, non-stationary industrial IoT streams* (manuscript sources, `references.bib`, `build.sh`, PDF/DOCX, supplementary file with the 66-paper corpus table) |
| `paper2/` | Paper 2: measurement study of first-order MAML on an LSTM autoencoder (manuscript sources, bibliography, build script, PDF/DOCX) |
| `damad/` | The DAMAD implementation and the benchmark harness both papers run through; see `damad/README.md` |
| `experiments/` | Study runners, table and figure generators, architecture-diagram script |
| `results/` | Result tables and summaries (per-run JSONL outputs are regenerated, not tracked) |
| `figures/` | All figures used in the manuscripts |
| `review/` | PRISMA-style review: raw IEEE Xplore and Lens.org exports, merge and screening scripts, decisions, corpus table |

Build a manuscript with `bash paper/build.sh` or `bash paper2/build.sh`
(pandoc, the IEEE CSL file in the folder, and a Chromium binary for the PDF).
