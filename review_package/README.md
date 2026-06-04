# Review Package Overview

This directory contains visual and tabular evidence for the OFDM-based RRAM
crossbar implementation and verification flow. The package is organized to make
the design-to-implementation path easy to inspect without reading the scripts
first.

## Contents

- `design_to_implementation_trace.pdf/png` summarizes the path from equations
  and circuit blocks to generated netlist, reusable testbench, Spectre results,
  and performance extraction.
- `bitline_readout_mapping_128x128.pdf/png` shows the implemented per-bitline
  readout path: RRAM bitline, readout/I-to-V interface, BPF bank,
  coherent-demodulation testbench, and I/Q integrated outputs.
- `netlist_structure_summary.csv/pdf/png` reports structural counts extracted
  from the generated 128 x 128 crossbar netlist.
- `testbench_structure_summary.csv/pdf/png` reports structural counts extracted
  from the reusable verification testbench.
- `waveform_overview_8x8.pdf/png`, `waveform_overview_32x32.pdf/png`, and
  `waveform_overview_128x128.pdf/png` provide waveform evidence for the three
  deployment scales.
- `signal_chain_example_bl000_carrier0.pdf/png` follows one concrete signal path
  from a bitline node through BPF and I/Q integration.
- `deployment_scaling_summary.csv/pdf/png` records execution status and runtime
  for 8 x 8, 32 x 32, and 128 x 128 deployments.
- `performance_extraction_trace.csv/pdf/png` lists the reported read-path
  metrics and their calculation basis.
- `read_state_estimate_explanation.md/pdf/png` explains the read-state estimate
  scope and the derivation of throughput, power, energy, and energy efficiency.

Use `review_package_index.md` as the linked index for the full package.
