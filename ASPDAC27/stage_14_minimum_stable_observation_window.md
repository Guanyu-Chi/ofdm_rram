# Stage 14 — Minimum stable observation window

- Completion time: 2026-07-16 16:05 CEST
- Scope: determine the minimum reproducible observation window for the four-carrier physical transient chain from completed single-carrier isolation waveforms.
- Input waveforms: `experiments/iccd2026_ofdm_rram/results/isolation_250_ascii`, `isolation_500_ascii`, `isolation_750_ascii`, and `isolation_1G_ascii`.
- Definition: an observation window is the contiguous post-recovery interval over which each recovered differential I/Q pair is averaged to form one carrier response vector.
- Timing basis: carrier periods are 4 ns (250 MHz), 2 ns (500 MHz), 4/3 ns (750 MHz), and 1 ns (1 GHz). The least shared integer-cycle interval is 4 ns, containing 1, 2, 3, and 4 cycles respectively. Candidate windows therefore used 4 ns multiples.
- Stability criterion: at several eligible post-switch placements, the maximum coefficient of variation of the four target I/Q vector amplitudes must not exceed the measured 8.18% uncalibrated four-code DAC step deviation. This keeps observation-window variation below the existing modulation-DAC uncertainty.
- Scan results: 4 ns: 14.70%; 8 ns: 12.39%; 12 ns: 10.47%; 16 ns: 8.79%; 20 ns: 7.29%; 24 ns: 5.87%.
- Decision: 20 ns is the minimum window satisfying the amplitude-stability criterion because it is the first 4 ns multiple below 8.18%. It is not yet the final system window for a strong-isolation claim.
- Isolation cross-check: the worst relative non-target response is 250 MHz to 750 MHz at -8.41 dB for 20 ns, -8.83 dB for 24 ns, and -9.31 dB for 28 ns. Window extension alone does not establish strong isolation.
- Limitation: this window is a property of the present public 45 nm compact-model transient chain and its specified code transition; it is not a universal OFDM symbol-period claim.
- Next reproducible action: retain 20 ns only as the minimum stability reference; improve physical receiver selectivity before choosing a final isolation-qualified system window and reporting power, energy, or throughput.
