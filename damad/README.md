# DAMAD — Drift-Aware Meta-Adaptive Detector

Reference implementation and benchmark harness for the paper
*Drift-aware meta-adaptive anomaly detection for few-shot, non-stationary
industrial IoT streams: a benchmarking protocol and the DAMAD detector*
(sources in `paper/`).  Everything runs on a CPU.  The full study covers
eight datasets (SWaT, WADI, HAI 21.03, SMAP, MSL, SMD, SKAB, PSM), nine
named methods plus nine ablations, five seeds, four injected drift patterns
and three support-set sizes, 19,650 scored streaming runs in all; it takes
about a day on four cores, and any subset of datasets or seeds can be run
on its own.

## Layout

```
damad/
  data/        download.py (fetch HAI, SMD, SKAB, PSM), loaders.py (one Entity per
               held-out stream for all eight datasets), windows.py, drift.py (sudden /
               gradual / incremental / recurring injection), tasks.py (regime segmentation
               and episodes), regimes.py (k-means regimes, used by the second study), cache.py
  models/      vae.py (functional MLP-VAE), meta.py (FOMAML, MAML++, Meta-SGD, static
               pretraining), lstm_ae.py and fomaml.py (second study, see below)
  online/      adwin.py, mmd.py, threshold.py (POT), memory.py (regime buffer),
               detector.py (the one streaming loop every method runs through)
  baselines/   registry.py (every method and ablation as a configuration), iforest.py
  eval/        metrics.py (point-wise P/R/F1, AUROC/AUPRC, latency, FPR under drift, adaptation steps)
experiments/
  run_all.py              the study; one job per (dataset, seed)
  make_tables.py          Markdown + LaTeX tables and results/summary.json
  make_figures.py         all figures
  draw_architectures.py   the architecture diagrams of both papers
  obj2/                   the second study (paper2/)
paper/, paper2/           manuscript sources, bibliographies and build scripts
```

## Reproduce

```bash
pip install torch numpy pandas scipy scikit-learn matplotlib
python -m damad.data.download            # HAI, SMD, SKAB, PSM: ~750 MB into data/raw
python experiments/run_all.py --workers 4  # all eight datasets, seeds 0-4
python experiments/make_tables.py
python experiments/make_figures.py
```

`run_all.py` takes `--datasets`, `--seeds`, `--methods`, `--drifts` and
`--shots` to run a subset, and `--quick` runs a few-iteration version of
everything in minutes as a smoke test.

Four datasets are not fetched by the download script:

* **SMAP and MSL.** Place the telemanom release under `data/raw/nasa/`
  (`train/<channel>.npy`, `test/<channel>.npy`, `labeled_anomalies.csv`).
* **SWaT and WADI.** These need a data-use agreement with iTrust (Singapore
  University of Technology and Design).  The loader expects, under
  `data/raw/swat/` and `data/raw/wadi/`, the normal and attack traces as
  `<name>_normal.npy` and `<name>_attack.npy` with `<name>_attack_labels.npy`,
  downsampled to 10 s by stride and MinMax-scaled on the normal trace.

If a dataset is missing, leave it out of `--datasets`; the tables and
figures are built from whatever results are present.

## How a method is defined

Every method is an `OnlineConfig` (see `damad/online/detector.py`).  The
streaming loop never looks ahead: scoring, drift confirmation, support-set
collection, adaptation, threshold recalibration and the champion/challenger
shadow period all happen in stream order, so the latency and adaptation
numbers in the paper are the numbers an operator would see.

| name       | init   | on drift           | gate            | replay | tau recal | notes                                   |
|------------|--------|--------------------|-----------------|--------|-----------|-----------------------------------------|
| IF         | –      | –                  | –               | –      | –         | Isolation Forest on windows             |
| VAE-S      | static | nothing            | –               | –      | –         | pooled normal data, one threshold       |
| VAE-FT     | static | fine-tune once     | –               | –      | –         | K-shot fine-tune at stream start        |
| VAE-INC    | static | SGD every 5 steps  | –               | –      | –         | Wahab-style online learning             |
| VAE-DFT    | static | fine-tune          | residual ADWIN  | –      | yes       | drift-aware, no meta-learning           |
| MAML-1     | meta   | nothing            | –               | –      | –         | MAVAE-style, adapt once                 |
| MSGD-1     | meta   | nothing            | –               | –      | –         | Meta-SGD initialisation, adapt once     |
| OML-A      | meta   | K-step adapt       | MMD on input    | –      | –         | OMLog idea on sensor streams            |
| DAMAD      | meta   | K-step adapt       | residual ADWIN  | yes    | yes       | proposed, with acceptance test          |

The nine ablations are variants of the DAMAD row: `DAMAD-noM1` and
`DAMAD-rndM1` change how meta-training episodes are drawn (contiguous
chunks, random windows), `DAMAD-noM3` drops replay, `DAMAD-noM4` drops
threshold recalibration, `DAMAD-noAcc` drops the champion/challenger
acceptance test, `DAMAD+mmd` and `DAMAD-mmd` change the gate (ADWIN with
MMD, MMD alone), and `DAMAD-fo` and `DAMAD-msgd` swap the meta-learner for
first-order MAML and Meta-SGD.

## Offline meta-learning study (paper2/)

A second study uses the same loaders, metrics and threshold rule for an
offline question: does an LSTM autoencoder trained with first-order MAML
actually train, adapt and detect?  Its code is `damad/models/lstm_ae.py`,
`damad/models/fomaml.py` (corrected FOMAML plus the broken-gradient-path
control), `damad/data/regimes.py` (k-means regimes as tasks) and
`experiments/obj2/`.

```
python experiments/obj2/run_obj2.py --workers 4            # 25 within-plant + 30 transfer jobs
python experiments/obj2/run_obj2.py --datasets hai,swat,wadi --seeds 0,1 --transfer 0 --outer 3000 --tag _long
python experiments/obj2/add_magnitude_baseline.py          # parameter-free reference rows
python experiments/obj2/make_tables_obj2.py                # results/obj2/tables, figures/obj2
```

Raw rows go to `results/obj2/*.jsonl` (not tracked); tables and the
meta-training logs (`results/obj2/meta_*.json`) are tracked.
