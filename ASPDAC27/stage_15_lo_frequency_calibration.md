# Stage 15 — LO frequency calibration

- Completion time: 2026-07-16 18:00 CEST
- Input: `tb/tb_ptm45_lo_characterization.scs`; output: `results/lo_characterization_ascii`.
- Baseline frequencies: 277.28, 550.65, 817.93, and 1086.13 MHz for nominal 250, 500, 750 MHz, and 1 GHz.
- Retuned input: `tb/tb_ptm45_lo_characterization_retuned.scs`; output: `results/lo_characterization_retuned_ascii`.
- Retuned ring loads: 421.5 fF, 209.25 fF, 138.50 fF, and 103.18 fF. Retuned quadrature capacitors: 4.436 pF, 2.203 pF, 1.455 pF, and 1.086 pF.
- Result: 250.15, 500.69, 751.35, and 1002.22 MHz; frequency errors 0.06%, 0.14%, 0.18%, and 0.22%. I-to-Q phases: 86.25, 88.92, 91.34, and 93.58 degrees.
- Decision: use the retuned LO settings for subsequent isolation measurements.
- Next action: apply the settings to the full physical four-carrier netlist and rerun single-carrier isolation.
