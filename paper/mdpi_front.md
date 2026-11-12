---
title: "Drift-Aware Meta-Adaptive Anomaly Detection for Few-Shot, Non-Stationary Industrial IoT Streams: A Benchmarking Protocol and the DAMAD Detector"
author:
  - "Abhijeet Chandrakant Karve ^1,^\\* and Santosh Darade ^1^"
  - "^1^ Department of Computer Science and Engineering, MIT Art, Design and Technology University, Rajbaug, Loni Kalbhor, Pune 412201, Maharashtra, India; ackarve11@gmail.com (A.C.K.); santosh.darade@mituniversity.edu.in (S.D.)"
  - "\\* Correspondence: ackarve11@gmail.com"
date: ""
bibliography: references.bib
csl: mdpi.csl
link-citations: true
---

**Abstract:** Industrial sensor streams must be monitored for faults with few labelled examples, under shifting distributions, and with new fault types appearing after deployment. A systematic review of 66 papers (2020–2025) found no method that joins meta-learning with online adaptation on a non-stationary stream and is tested on an industrial benchmark. We close that gap in three steps: a four-dimensional taxonomy with a benchmarking protocol with point-wise metrics, controlled drift injection and three streaming measures; DAMAD, a drift-aware meta-adaptive detector that pairs a variational autoencoder initialised by model-agnostic meta-learning (MAML++) with a residual-side drift gate, regime replay, a gated extreme-value threshold and a champion/challenger acceptance test; and an evaluation against eight baselines on eight public industrial and telemetry benchmarks over five seeds, four drift patterns and ten ablations, 19,650 streaming runs. Without drift, a static autoencoder matches the meta-learned detectors on six of the eight datasets. Under drift, static and adapt-once detectors alarm on 73 to 87 % of normal steps and never recover; DAMAD holds the rate at 17 to 30 %, recovers within 230 to 440 windows and has the best pooled F1 under every pattern. Threshold recalibration and the residual-side gate carry the result; the choice of meta-learner is secondary.

**Keywords:** meta-learning; few-shot learning; anomaly detection; industrial Internet of Things; concept drift; streaming data; variational autoencoder; benchmarking

