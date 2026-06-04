# Read-State Estimate Explanation

## Definition

Read state refers to the inference/read operation of the programmed RRAM crossbar. During this operation, each RRAM cell remains in its fixed programmed conductance state and the wordline stimulus is applied to evaluate the column response. The generated 128×128 netlist uses binary programmed conductance states with Ron = 1 kOhm and Roff = 1 MOhm, together with MOS selectors and fixed read-mode connectivity.

## Why the Estimate Uses Read State

The evaluated architecture targets inference execution on a programmed RRAM crossbar. Inference repeatedly uses the already-programmed conductance matrix; write, erase, forming, and training-time update operations are outside this read-path evaluation. The reported latency, throughput, read-state power, energy per window, and energy efficiency therefore describe the active crossbar read operation used for analog MVM evaluation.

This scope is sufficient for the current implementation evidence because the generated Spectre netlist and reusable verification testbench validate the read-path behavior: wordline excitation, bitline accumulation, per-bitline readout observation, BPF separation, coherent demodulation, and I/Q integration. Chip-level peripheral power, programming overhead, and package-level system overhead are not included in the read-state estimate.

## How the Read-State Power Is Estimated

The estimate is computed from the generated 128×128 conductance matrix in `config/G_matrix_seed2026.csv`. Each cell conductance `G_ij` is either Ron-derived or Roff-derived:

- Ron cells: 8355
- Roff cells: 8029
- Total cells: 16384

The configured read voltage levels are `[-0.3, -0.1, 0.3, 0.1]` V. The mean squared read voltage used by the estimate is:

`mean(V^2) = ((-0.3)^2 + (-0.1)^2 + (0.3)^2 + (0.1)^2) / 4 = 0.050 V^2`

The average read-state crossbar power is then calculated as:

`P_read = sum(G_ij) x mean(V^2) = 4.181515e-01 W`

## Throughput and Energy Chain

The transient read window is 80 ns. The operation count uses the generated 128×128 deployment, four simultaneous carriers, and one multiply plus one accumulation counted as two operations:

`Ops/window = 128 x 128 x 4 x 2 = 131072`

The resulting throughput is:

`Throughput = 131072 / 80 ns = 1.638400e+12 ops/s`

The energy per read window is:

`Energy/window = P_read x 80 ns = 3.345212e-08 J`

The energy per operation is:

`Energy/op = Energy/window / Ops/window = 2.552194e-13 J/op`

The read-state energy efficiency is:

`Energy efficiency = Throughput / P_read = 3.918198 TOPS/W`

## Scope Statement

These values are crossbar read-state metrics extracted or estimated from the generated 128×128 RRAM crossbar instance and its associated verification environment. They do not represent full-chip energy efficiency or complete peripheral implementation power.
