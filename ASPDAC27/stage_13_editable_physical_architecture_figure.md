# Stage 13 — Editable physical architecture figure

- Completion time: 2026-07-16 15:49 CEST
- Scope: local editable architecture figure describing the implemented four-carrier physical peripheral and the separate mapped-crossbar evaluation boundary. No manuscript source or external project was modified.
- Source: `experiments/iccd2026_ofdm_rram/results/figures/make_physical_architecture_ppt.py`.
- Outputs: `experiments/iccd2026_ofdm_rram/results/figures/physical_fourcarrier_architecture.pptx` and `experiments/iccd2026_ofdm_rram/results/figures/physical_fourcarrier_architecture.pdf`.
- Reproduction: `PYTHONPATH=/tmp/pptx_deps python3 experiments/iccd2026_ofdm_rram/results/figures/make_physical_architecture_ppt.py`, followed by `libreoffice --headless --convert-to pdf --outdir experiments/iccd2026_ofdm_rram/results/figures experiments/iccd2026_ofdm_rram/results/figures/physical_fourcarrier_architecture.pptx`.
- Contents: 2-bit input, four PMOS DAC cells, ring LO and quadrature network, wordline driver, RRAM crossbar, selected bitline TIA, four I/Q receiver pairs, sample-and-hold, one-bit decisions, and subsequent digital logic.
- Limitation: the drawing states implementation topology, not a completed four-carrier isolation or energy measurement.
- Next reproducible action: after owner approval, copy the PDF to the manuscript tree and replace the existing Fig. 4 artwork and caption with the scoped physical architecture description.
