# Stage 11 — Physical four-code DAC sweep

- Completion time: 2026-07-16 15:12 CEST
- Scope: Local transistor-level Spectre calibration of the PMOS 2-bit modulation DAC in the integrated four-carrier receiver testbench. No repository synchronization or manuscript change was performed.
- Input netlists: `experiments/iccd2026_ofdm_rram/tb/tb_ptm45_dac2_fourcode.scs` (500 nm), `experiments/iccd2026_ofdm_rram/tb/tb_ptm45_dac2_fourcode_w350.scs`, and `experiments/iccd2026_ofdm_rram/tb/tb_ptm45_dac2_fourcode_w650.scs`.
- Model and command: public 45 nm compact-model files included by each netlist; `spectre -format nutascii -raw <result_dir> <netlist>`.
- Output paths: `experiments/iccd2026_ofdm_rram/results/dac2_fourcode_ascii`, `experiments/iccd2026_ofdm_rram/results/dac2_fourcode_w350_ascii`, and `experiments/iccd2026_ofdm_rram/results/dac2_fourcode_w650_ascii`.
- Check: averaged `tiaout` over phase-aligned two-cycle windows 8–16 ns, 20–28 ns, 36–44 ns, and 52–60 ns for codes 00, 01, 10, and 11.

| MSB PMOS width | Code levels 00/01/10/11 (mV) | Consecutive steps (mV) | Maximum step deviation |
|---:|---:|---:|---:|
| 350 nm | 43.583 / 102.915 / 135.412 / 189.383 | 59.332 / 32.497 / 53.971 | 33.13% |
| 500 nm | 43.584 / 102.916 / 168.032 / 216.729 | 59.332 / 65.116 / 48.697 | 15.62% |
| 650 nm | 43.584 / 102.916 / 195.830 / 239.678 | 59.332 / 92.914 / 43.847 | 42.15% |

- Decision: retain the 500 nm MSB PMOS width. It is monotonic and has the smallest observed phase-aligned four-code step error among the tested widths.
- Limitation: this verifies recovered `tiaout` code levels in the complete transient chain, not a stand-alone static DAC transfer curve; do not make a calibrated-linearity claim.
- Next reproducible action: perform a narrow 450/500/550 nm sweep only if a lower step-error target is required, then export time-domain traces for the physical-waveform figure.
