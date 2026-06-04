# Review Package Index

This package collects design and implementation evidence for the OFDM-based RRAM crossbar verification flow. Each item links a design block to generated implementation files, simulation outputs, or extracted results.

## 1. Design-to-Implementation Trace

- [design_to_implementation_trace.pdf](design_to_implementation_trace.pdf)
- [design_to_implementation_trace.png](design_to_implementation_trace.png)

This figure summarizes the full path from equations and circuit blocks to generated netlist, reusable testbench, Spectre results, and performance extraction.

## 2. Circuit Design Mapping

- [circuit_design_mapping.md](circuit_design_mapping.md)
- [bitline_readout_mapping_128x128.pdf](bitline_readout_mapping_128x128.pdf)
- [bitline_readout_mapping_128x128.png](bitline_readout_mapping_128x128.png)

The implemented readout path is organized as:

`RRAM bitline` → `Readout / I-to-V interface` → `BPF bank` → `Coherent-demodulation testbench` → `I/Q integrated outputs`

For the 128×128 deployment, the verification chain contains 128 bitlines and four carrier paths per bitline, resulting in 512 BPF/demodulation paths and 1024 I/Q integrated outputs.

## 3. Netlist Structural Summary

- [netlist_structure_summary.csv](netlist_structure_summary.csv)
- [netlist_structure_summary.pdf](netlist_structure_summary.pdf)
- [netlist_structure_summary.png](netlist_structure_summary.png)

This table checks wordlines, bitlines, RRAM cells, MOS selectors, Ron/Roff states, and bitline loads extracted from the generated 128×128 netlist.

## 4. Testbench Structural Summary

- [testbench_structure_summary.csv](testbench_structure_summary.csv)
- [testbench_structure_summary.pdf](testbench_structure_summary.pdf)
- [testbench_structure_summary.png](testbench_structure_summary.png)

This table checks the reusable verification testbench structure, including BPF paths, I/Q demodulation segments, integration outputs, saved output nodes, and the 80 ns transient window.

## 5. Waveform Evidence

- [waveform_overview_8x8.pdf](waveform_overview_8x8.pdf)
- [waveform_overview_8x8.png](waveform_overview_8x8.png)
- [waveform_overview_32x32.pdf](waveform_overview_32x32.pdf)
- [waveform_overview_32x32.png](waveform_overview_32x32.png)
- [waveform_overview_128x128.pdf](waveform_overview_128x128.pdf)
- [waveform_overview_128x128.png](waveform_overview_128x128.png)
- [signal_chain_example_bl000_carrier0.pdf](signal_chain_example_bl000_carrier0.pdf)
- [signal_chain_example_bl000_carrier0.png](signal_chain_example_bl000_carrier0.png)

The overview figures show selected bitline, BPF, and I/Q integrated outputs for 8×8, 32×32, and 128×128 deployments. The signal-chain figure follows one concrete path: `bl000`, `bpf_c000_0`, `Icar_c000_0`, and `Qcar_c000_0`.

Existing full-bitline waveform exports are kept in the simulation result directories:

- `results/sanity_8x8/waveform_8x8_bitlines.pdf/png`
- `results/sanity_32x32/waveform_32x32_bitlines.pdf/png`
- `results/sim_run_zerowarn/waveform_128x128_bitlines.pdf/png`

## 6. Deployment Scaling Summary

- [deployment_scaling_summary.csv](deployment_scaling_summary.csv)
- [deployment_scaling_summary.pdf](deployment_scaling_summary.pdf)
- [deployment_scaling_summary.png](deployment_scaling_summary.png)

This file records the 8×8, 32×32, and 128×128 Spectre execution status and elapsed runtime extracted from the corresponding simulation logs.

## 7. Performance Extraction Trace

- [performance_extraction_trace.csv](performance_extraction_trace.csv)
- [performance_extraction_trace.pdf](performance_extraction_trace.pdf)
- [performance_extraction_trace.png](performance_extraction_trace.png)

This table lists the performance metrics reported by the extraction stage and keeps the source field attached to each value.

## 8. Read-State Estimate Explanation

- [read_state_estimate_explanation.md](read_state_estimate_explanation.md)
- [read_state_estimate_explanation.pdf](read_state_estimate_explanation.pdf)
- [read_state_estimate_explanation.png](read_state_estimate_explanation.png)

This file defines read state, explains why the current evaluation reports read-path metrics, and shows how read-state power, energy per window, energy per operation, throughput, and TOPS/W are calculated from the generated 128×128 conductance matrix and the 80 ns read window.
