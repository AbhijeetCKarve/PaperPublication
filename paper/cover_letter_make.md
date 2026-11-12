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

**Why the work matters.** Industrial sensor streams have to be monitored for faults with almost no labelled examples, under distributions that keep moving, and with new fault types appearing after deployment. Meta-learning is the standard answer to the few-shot part of that problem, and concept-drift detection to the non-stationary part, but the two literatures have not met. A systematic review of 66 peer-reviewed papers from 2020 to 2025, built from IEEE Xplore and Lens.org exports with every screening decision released, shows that no published method combines meta-learning with online adaptation on a non-stationary stream and is evaluated on an industrial benchmark. The manuscript fills that gap with a benchmarking protocol and with DAMAD, a working detector built on a MAML++-initialised variational autoencoder with a residual-side drift gate, regime replay, a gated extreme-value threshold and a champion/challenger acceptance test.

**What the findings add to existing work.** The evaluation covers eight baselines on eight public benchmarks (SWaT, WADI, HAI, SMAP, MSL, SMD, SKAB and PSM) over five seeds, four drift patterns and ten ablations, 19,650 streaming runs in total. Two results go against the current direction of the field. Without drift, a static autoencoder is as good as any meta-learned detector on six of the eight datasets, so the meta-learned initialisation is not the bottleneck that prior work assumes. Under drift, static and adapt-once detectors raise alarms on 73 to 87 % of normal steps and never recover, while DAMAD holds the rate at 17 to 30 % and recovers within a few hundred windows, and the ablations trace that gain to threshold recalibration and the residual-side gate rather than to the choice of meta-learner. The paper reports the cases where the method does not help as fully as those where it does.

**Why the journal.** The contribution is about learning under distribution shift from few examples, which is a machine-learning question rather than a sensing one, and the review, the taxonomy and the protocol are tools for extracting reliable knowledge from a fast-growing and loosely evaluated literature. Every number can be regenerated from the released code, loaders and configuration files, in line with the journal's emphasis on reproducible methodology.

This manuscript has not been submitted to any MDPI journal before. We confirm that neither the manuscript nor any parts of its content are currently under consideration for publication with or published in another journal. All authors have approved the manuscript and agree with its submission to MAKE.

Both authors are at MIT Art, Design and Technology University, Pune. We have no conflicts of interest to declare and the work received no external funding. The use of an AI assistant in preparing the text and code is disclosed in the Acknowledgments and in Section 6.3 of the manuscript.

Yours sincerely,

Abhijeet Chandrakant Karve, on behalf of the authors
