---
title: "Does a Meta-Learned Autoencoder Actually Adapt? A Measurement Study of First-Order MAML for Few-Shot Anomaly Detection on Industrial and Spacecraft Telemetry"
author:
  - "Abhijeet Chandrakant Karve ^1,^\\* and Santosh Darade ^1^"
  - "^1^ Department of Computer Science and Engineering, MIT Art, Design and Technology University, Rajbaug, Loni Kalbhor, Pune 412201, Maharashtra, India; ackarve11@gmail.com (A.C.K.); santosh.darade@mituniversity.edu.in (S.D.)"
  - "\\* Correspondence: ackarve11@gmail.com"
date: ""
bibliography: references.bib
csl: mdpi.csl
link-citations: true
---

**Abstract:** Meta-learning is often proposed to give an industrial anomaly detector a few-shot start in a new operating regime, and the evidence offered is usually a score table for the adapted model. Such a table cannot show whether the meta-learner trained, whether K-shot adaptation changed the model, or how much of the score the model contributed. We measured all three for an LSTM autoencoder trained with first-order model-agnostic meta-learning (MAML) on regimes carved from normal operation, on five public benchmarks (SWaT, WADI, HAI 21.03, SMAP and MSL), with five seeds, support sizes from 1 to 100 windows, within-plant and cross-plant evaluation, point-wise metrics and a label-free threshold; every comparison is a paired test over 11,180 result cells. Four instruments extend the usual protocol: the meta-update norm, with a control that reproduces a common gradient-path fault; the parameter change and score rank correlation before and after adaptation; a parameter-free window-magnitude reference; and a task-diversity score. The fault leaves no trace in the loss curve but zeroes the update norm in all 25 control runs. Adaptation moves the network by 0.1–0.6 % and barely changes the score ranking. The meta-learned detector never beats a static autoencoder by more than 0.01 AUROC, and on four benchmarks no autoencoder beats the window magnitude. We propose five measurements that any report of a meta-learned detector should include.

**Keywords:** meta-learning; MAML; LSTM autoencoder; anomaly detection; industrial control systems; spacecraft telemetry; few-shot adaptation; evaluation methodology

