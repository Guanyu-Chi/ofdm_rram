# Stage 07: Integrated physical signal-chain check

- Status: complete with quantified output-interface limitation
- Completed: 2026-07-16 10:39:49 CEST
- Scope: connect physical modulation cells, one bitline TIA, four I/Q receiver branches, transmission-gate sampling, and clocked decision circuitry.

## Files and command

- Single-lane integration: `../experiments/iccd2026_ofdm_rram/tb/tb_ptm45_integrated_lane_250m.scs`
- Four-carrier integration: `../experiments/iccd2026_ofdm_rram/tb/tb_ptm45_integrated_fourcarrier.scs`
- Four-carrier output waveform: `../experiments/iccd2026_ofdm_rram/results/ptm45_integrated_fourcarrier/tran.tran.tran`
- Four-carrier simulator log: `../experiments/iccd2026_ofdm_rram/results/ptm45_integrated_fourcarrier/run.log`

```bash
spectre experiments/iccd2026_ofdm_rram/tb/tb_ptm45_integrated_fourcarrier.scs +escchars +log experiments/iccd2026_ofdm_rram/results/ptm45_integrated_fourcarrier/run.log -format psfascii -raw experiments/iccd2026_ofdm_rram/results/ptm45_integrated_fourcarrier
```

## Physical chain

Four PMOS current cells are amplitude-controlled by independent baseband test fixtures and switched by their corresponding physical carrier paths. Their currents sum at one bitline. A PMOS common-gate TIA produces a single-ended output, which is capacitively coupled around a physical resistor-divider common mode and applied to eight physical Gilbert I/Q mixers. Each differential baseband output is sampled through CMOS transmission gates onto 100 fF capacitors. Clocked differential slicers and a subsequent transmission-gate output-hold interface provide the initial digital-domain handoff structure.

## Verified results

- The final 80 ns four-carrier transient completed with 0 errors.
- The four mixer differential means over the final 40 ns were: I = -7.92 mV, -8.82 mV, -2.63 mV, and -3.22 mV; Q = -5.27 mV, -2.20 mV, -3.23 mV, and -5.02 mV, ordered from low to high carrier group.
- In the single-lane test, held I samples changed from -2.61 mV and -5.34 mV before the baseband step to -30.38 mV, -48.53 mV, -56.29 mV, and -65.88 mV after the step, establishing physical modulation, TIA conversion, demodulation, and sampling continuity.
- The four-carrier test uses no behavioral readout element or RLC band-pass readout.

## Output-interface limitation

The present slicer directly receives only a few millivolts of differential baseband signal. Its dynamic decision is therefore not reliably regenerated for every carrier and sample time. The transmission-gate sampler itself is physical and working, but the resulting one-bit decision must not be reported as a validated converter result.

The required next circuit is a physical differential baseband preamplifier between each I/Q sample-hold pair and the clocked slicer. A multi-bit conversion claim remains unsupported until that preamplifier and converter resolution are simulated.

## Numerical-model warning

The log retains six startup model warnings and thirteen notices. The first warning occurs at tens of attoseconds during initialization; it is not a clean-warning result and must be reported as a compact-model startup limitation.
