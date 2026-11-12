**Abhijeet Chandrakant Karve**
Department of Computer Science and Engineering
MIT Art, Design and Technology University, Pune, India
ackarve11@gmail.com

12 November 2026

Editor-in-Chief
*Machine Learning and Knowledge Extraction*
MDPI

Dear Editor,

Please consider the enclosed manuscript, "Drift-Aware Meta-Adaptive Anomaly Detection for Few-Shot, Non-Stationary Industrial IoT Streams: A Benchmarking Protocol and the DAMAD Detector", for publication as an Article in the Learning section of *Machine Learning and Knowledge Extraction*.

The paper asks a plain question: when an industrial sensor stream has to be monitored with almost no labelled faults and its distribution keeps moving, does meta-learning help, and under what conditions? We answer it in three parts. A systematic review of 66 peer-reviewed papers from 2020 to 2025, built from IEEE Xplore and Lens.org exports with every screening decision released, shows that no published method combines meta-learning with online adaptation on a non-stationary stream and is evaluated on an industrial benchmark. A benchmarking protocol with strictly point-wise metrics, controlled drift injection and three streaming measures makes such methods comparable. And DAMAD, a working detector built on a MAML++-initialised variational autoencoder with a residual-side drift gate, regime replay, a gated extreme-value threshold and a champion/challenger acceptance test, is evaluated against eight baselines on eight public benchmarks over five seeds, four drift patterns and ten ablations, 19,650 streaming runs in total.

We think the paper suits this journal for two reasons. The contribution is about learning under distribution shift with few examples, which is a machine-learning question rather than a sensing one, and the results are reported in full, including where the method does not help: without drift a static autoencoder is as good as any meta-learned detector on six of the eight datasets, and the gain under drift comes from the threshold and the gate rather than from the meta-learner. Every number in the paper can be regenerated from the released code, loaders and configuration files.

An early conceptual version of the taxonomy and the detector design was presented at the PCEMS 2026 conference. The present manuscript rebuilds the review from the raw database exports, implements the system, reports all experiments for the first time, and revises two design decisions on the basis of that evidence; none of the results has been published before. The manuscript is not under consideration elsewhere, and all authors have approved the submission.

Both authors are at MIT Art, Design and Technology University, Pune. We have no conflicts of interest to declare and the work received no external funding.

Yours sincerely,

Abhijeet Chandrakant Karve, on behalf of the authors
