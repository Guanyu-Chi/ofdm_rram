# Current handoff

- Time: 2026-07-16 16:51 CEST
- Workspace: `/nas/ei/share/TUEIEDAscratch/ge86duw/ICCD`; branch `main`; no commits yet.
- Records: `ASPDAC27/INDEX.md`, stages 11–14, and `checkpoint_01.md`.
- Important directories: `experiments/iccd2026_ofdm_rram/tb` (netlists), `experiments/iccd2026_ofdm_rram/results` (raw transient output), `experiments/iccd2026_ofdm_rram/results/figures` (all newly generated figure source/images), `ASPDAC27/overleaf` (manuscript).
- Final DAC configuration: `tb_ptm45_integrated_fourcarrier.scs`, MCS1 PMOS width 450 nm, length 90 nm.
- Baseline outputs: `results/integrated_fourcarrier_w450_ascii`; isolation outputs `results/isolation_250_ascii`, `isolation_500_ascii`, `isolation_750_ascii`, `isolation_1G_ascii`.
- Current run: `spectre -format nutascii -raw experiments/iccd2026_ofdm_rram/results/lo_characterization_ascii experiments/iccd2026_ofdm_rram/tb/tb_ptm45_lo_characterization.scs`.
- Window result: 20 ns is the first 4 ns multiple with worst amplitude CV below 8.18%; it is not a final strong-isolation window.
- Isolation result: worst baseline non-target response is 250 MHz to 750 MHz, -8.41 dB at 20 ns.
- Rejected prototype: `tb_ptm45_isolation_250_selective.scs`; passive LC selectivity caused severe target attenuation and must not be copied.
- Generated figures: `results/figures/physical_dac_fourcode_waveforms.{png,pdf}`, `results/figures/physical_fourcarrier_architecture.{pptx,pdf}`; sources are in the same directory.
- Manuscript: no pending physical-window or architecture changes have been synchronized. Before any manuscript or external synchronization, inspect exact files, audit terminology/author fields, report scope, and obtain explicit approval.
- Immediate next: parse LO actual frequency and quadrature phase from `lo_characterization_ascii`; use that result before designing a high-input-impedance selective receiver.
