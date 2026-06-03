# ofdm_rram

`ofdm_rram` contains a reproducible experiment framework for OFDM-based readout evaluation on RRAM crossbar arrays. The project generates binary-conductance crossbar matrices, Spectre-compatible crossbar netlists, reusable transient testbenches, structural checks, and read-window performance summaries.

## What is included

- Configurable 8x8, 32x32, and 128x128 RRAM crossbar cases.
- Binary Ron/Roff conductance matrix generation with a fixed seed.
- OFDM carrier stimulus generation with cosine and sine I/Q branches.
- Spectre netlists for programmed read-state crossbar evaluation.
- Reusable testbenches for carrier-selective readout verification.
- Structural checks for generated netlist and testbench artifacts.
- Read-window performance extraction for latency, throughput, power, energy, and energy efficiency.

## Repository layout

```text
config/      Experiment configuration and generated conductance matrices
netlist/     Generated Spectre crossbar netlists
tb/          Reusable Spectre testbenches
scripts/     Matrix, netlist, testbench, checking, and performance scripts
results/     Compact CSV summaries from generated checks and estimates
```

## Requirements

- Python 3.8 or newer
- Cadence Spectre, for running the provided `.scs` testbenches

The Python scripts use the standard library only.

## Typical workflow

```bash
python3 scripts/gen_matrix.py
python3 scripts/gen_netlist.py
python3 scripts/gen_sanity_cases.py
python3 scripts/gen_testbench.py --size 128 --final
python3 scripts/structural_check.py
python3 scripts/calc_performance.py
```

Spectre runs can be launched with:

```bash
scripts/run_sanity_spectre.sh 8
scripts/run_sanity_spectre.sh 32
scripts/run_spectre.sh
```

## Result scope

The reported performance metrics are read-window estimates for the generated RRAM crossbar instance and its verification environment. Power and energy values are resistor-level read-state estimates based on the programmed Ron/Roff conductance matrix and configured read stimulus. Chip-level peripheral power is not included.
