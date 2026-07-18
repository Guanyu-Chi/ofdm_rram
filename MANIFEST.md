# ofdm_rram Publication File Manifest

This document lists the files selected for the standalone `ofdm_rram` project release.

## Included Files

- `.gitignore`
- `README.md`
- `config/G_matrix_seed2026.csv`
- `config/G_matrix_seed2026_32x32.csv`
- `config/G_matrix_seed2026_8x8.csv`
- `config/ofdm_rram_config.yaml`
- `netlist/clean_128x128_crossbar.scs`
- `netlist/clean_32x32_crossbar_sanity.scs`
- `netlist/clean_8x8_crossbar_sanity.scs`
- `results/bpf_response.csv`
- `results/performance_summary.csv`
- `results/sanity_summary.csv`
- `results/structural_check.csv`
- `scripts/calc_bpf_response.py`
- `scripts/calc_performance.py`
- `scripts/gen_matrix.py`
- `scripts/gen_netlist.py`
- `scripts/gen_sanity_cases.py`
- `scripts/gen_testbench.py`
- `scripts/parse_results.py`
- `scripts/run_sanity_spectre.sh`
- `scripts/run_spectre.sh`
- `scripts/structural_check.py`
- `tb/tb_ofdm_qam_128x128.scs`
- `tb/tb_ofdm_qam_128x128_zerowarn.scs`
- `tb/tb_ofdm_qam_32x32_sanity.scs`
- `tb/tb_ofdm_qam_8x8_sanity.scs`

## Excluded Content

- Draft-writing folders and manuscript assets.
- Patch reports, reviewer notes, and draft-specific documents.
- Raw Spectre PSF waveform directories and transient binary outputs.
- Absolute-path simulator logs.
- Local editor/server files and virtual environments.
- Unrelated historical projects in the workspace.

## Release Audit Policy

The release candidate is checked for project-external tooling references before upload. No project-external workspace metadata should appear in the release candidate.

## v5 Four-Channel Transistor-Chain Artifacts (added 2026-07-18)

Final calibrated four-channel peripheral-chain experiment
(carriers 250/500/750/1000 MHz, error <= 0.22%; see
`experiments/iccd2026_ofdm_rram/results/figures/EXPERIMENT_SUMMARY.md`).

- `experiments/iccd2026_ofdm_rram/tb/tb_ptm45_filteronly_{250,425,723,1229}.scs` — single-tone runs (differ only in DAC enable bits)
- `experiments/iccd2026_ofdm_rram/tb/tb_ptm45_filteronly_4tone.scs` — four-tone run
- `experiments/iccd2026_ofdm_rram/tb/tb_ptm45_filteronly_4tone_pwr.scs` — four-tone power run (adds `save VDD:p` only)
- `experiments/iccd2026_ofdm_rram/tb/tb_ptm45_ringcal.scs` — 60 ns ring-oscillator calibration bench
- `experiments/iccd2026_ofdm_rram/tb/tb_ptm45_filter_ac.scs` — in-situ AC response bench
- `experiments/iccd2026_ofdm_rram/results/figures/*.py` — nutascii parsing, leakage matrix, ideal demodulation, Gilbert metrics, figure generation
- `experiments/iccd2026_ofdm_rram/results/figures/*_v5.csv`, `oscillator_calibration.csv`, `power_4tone_v5.csv`, `filter_ac_response_final.csv`, `ideal_demod_4tone.csv` — result tables
- `experiments/iccd2026_ofdm_rram/results/figures/ideal_demod_waveforms/baseband_stim*_v5.csv` — baseband integration traces
- `experiments/iccd2026_ofdm_rram/results/figures/fig_*.png` — paper figures
- Raw Spectre nutascii waveform dumps remain excluded (multi-hundred-MB; regenerate with the listed netlists and commands in `EXPERIMENT_SUMMARY.md`).
