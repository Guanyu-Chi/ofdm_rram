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
