# Physical signal-chain reproduction

This directory contains the minimal files needed to reproduce the four-carrier physical signal-chain check in `../../ASPDAC27/stage_07_integrated_signal_chain.md`.

## Required files

- `models/ptm45/`: public predictive 45 nm compact-model cards.
- `tb/tb_ptm45_integrated_fourcarrier.scs`: four modulation cells, shared bitline TIA, eight I/Q mixers, sample-and-hold cells, and clocked decision interface.

## Command

From the repository root, after configuring the local Spectre environment:

```bash
mkdir -p experiments/iccd2026_ofdm_rram/results/ptm45_integrated_fourcarrier
spectre experiments/iccd2026_ofdm_rram/tb/tb_ptm45_integrated_fourcarrier.scs +escchars +log experiments/iccd2026_ofdm_rram/results/ptm45_integrated_fourcarrier/run.log -format psfascii -raw experiments/iccd2026_ofdm_rram/results/ptm45_integrated_fourcarrier
```

The present clocked slicer is an interface study. Its low-signal limitation is documented in Stage 07; it is not a validated multi-bit converter.

## Four-code DAC waveform reproduction

The final MSB PMOS DAC cell is 450 nm wide and 90 nm long in `tb/tb_ptm45_integrated_fourcarrier.scs`. Run the four-code test with Spectre using `tb/tb_ptm45_dac2_fourcode_w450.scs`, then generate the publication waveform with:

```bash
python3 experiments/iccd2026_ofdm_rram/results/figures/plot_physical_dac_waveforms.py
```

The editable architecture source and derived assets are in `results/figures/`: `make_physical_architecture_ppt.py`, `physical_fourcarrier_architecture.pptx`, and `physical_fourcarrier_architecture.pdf`. Raw transient output is intentionally not versioned; stages 11–14 record the input netlists, window extraction method, numerical results, and limitations.
