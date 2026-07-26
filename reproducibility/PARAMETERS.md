# Frozen Circuit Parameters

All values below are the final ("v5") frozen parameters used for every reported
result. They appear verbatim in the netlists under `netlists/`.

## Carriers (three-stage ring oscillators, `ring3`)

| Channel | Nominal | Load cap `cload` | Measured | Error |
|---------|---------|------------------|----------|-------|
| ch1 | 250 MHz | 925.9 fF | 249.50 MHz | -0.20% |
| ch2 | 500 MHz | 456.7 fF | 498.92 MHz | -0.22% |
| ch3 | 750 MHz | 300.1 fF | 748.86 MHz | -0.15% |
| ch4 | 1000 MHz | 221.8 fF | 998.70 MHz | -0.13% |

Quadrature phase-shifter caps (`qphase cphase`, zero-crossing-delay design
RC = T/(4 ln 2)): 1.443 p / 722 f / 481 f / 361 f for ch1..ch4.

## Filter bank

- ch1: 4th-order Butterworth low-pass `butterworth250`
  (L1 = 487.2 nH, L3 = 1.176 uH; C2 = 1.176 pF, C4 = 487.2 fF; 1 kohm terminations), corner 250 MHz.
- ch2/ch3/ch4: `tuned_select` LC band-pass, lval = 20 nH, cpl = 500 fF,
  cval = 4.841 p / 1.961 p / 1.059 p (centers 500 / 750 / 1000 MHz).

## RRAM cell (compact 1T1R)

- LRS `R_on` = 1 kohm, HRS `R_off` = 1 Mohm (binary conductance, read-path model).
- Selector: PMOS w = 270 n / l = 45 n, gate = active-low read enable.
- WL driver low-pass: two-section RC (10 kohm + per-channel cap) suppressing
  the square-wave harmonics that collide with the integer-multiple carrier grid.

## Receive chain

- TIA: common-gate PMOS + 5 kohm transimpedance, 10 fF load.
- Buffer: NMOS differential pair, 7 kohm loads.
- Gilbert demodulator: doubly balanced, 5 kohm loads, 2 pF integration cap;
  eight cells per sensed bitline (I and Q x 4 channels).

## Timing

- Supply VDD = 1.1 V; transient `tran stop=200n maxstep=1p skipdc=no`.
- Coherent integration window: 20 ns = 5 / 10 / 15 / 20 carrier cycles.
- Decision window opens at 160 ns (after the band-select filter settling,
  tau = 2Q/omega0 ~ 40 ns).

## Measured summary

- Filter-only diagonal amplitudes: 40.7 / 145.4 / 93.7 / 66.5 mV.
- Ideal decision margins: 24.0 / 17.4 / 3.67 / 20.8; Gilbert: 9.9 / 15.2 / 2.96 / 9.3.
- 4x4 MVM: ON 14.0 uA (spread 16.6%), OFF <= 2.07 uA (14.8% of ON).
- Four-tone steady-state power: 14.43 mW (idle 13.58 mW).
