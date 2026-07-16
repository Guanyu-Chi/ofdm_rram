# Stage 12 — Physical DAC waveform export

- Completion time: 2026-07-16 15:30 CEST
- Scope: selected the final modulation-DAC MSB PMOS width from the narrow physical sweep and exported a publication-format transient waveform figure locally.
- Final circuit: `experiments/iccd2026_ofdm_rram/tb/tb_ptm45_integrated_fourcarrier.scs`, with `MCS1` set to 450 nm width and 90 nm length.
- Sweep inputs and outputs: `tb/tb_ptm45_dac2_fourcode_w450.scs` -> `results/dac2_fourcode_w450_ascii`; `tb/tb_ptm45_dac2_fourcode.scs` -> `results/dac2_fourcode_ascii`; `tb/tb_ptm45_dac2_fourcode_w550.scs` -> `results/dac2_fourcode_w550_ascii`.
- Command: `spectre -format nutascii -raw <result_dir> <netlist>`.
- Evaluation: phase-aligned two-cycle windows at 8–16 ns, 20–28 ns, 36–44 ns, and 52–60 ns. The 450 nm choice produces `tiaout` levels of 43.584, 102.916, 157.701, and 208.129 mV; consecutive steps are 59.332, 54.785, and 50.427 mV; maximum step deviation is 8.18%.
- Plot script: `experiments/iccd2026_ofdm_rram/results/figures/plot_physical_dac_waveforms.py`.
- Figure outputs: `experiments/iccd2026_ofdm_rram/results/figures/physical_dac_fourcode_waveforms.png` and `experiments/iccd2026_ofdm_rram/results/figures/physical_dac_fourcode_waveforms.pdf`.
- Reproduction: generate `results/dac2_fourcode_w450_ascii` with the stated Spectre command, then run `python3 experiments/iccd2026_ofdm_rram/results/figures/plot_physical_dac_waveforms.py`.
- Limitation: public 45 nm compact model; waveform-level circuit operation only. The 8.18% figure is an uncalibrated recovered-output step error, not a static DAC INL/DNL specification.
- Next reproducible action: after owner approval, copy the PNG to the manuscript tree, replace the reserved verification placeholder with a blue figure and scoped description, compile, and run publication checks before external synchronization.
