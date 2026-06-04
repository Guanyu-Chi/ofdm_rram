# Circuit Design and Implementation Mapping

## Readout Structure

The implemented 128×128 crossbar exposes one independent bitline node per column. The generated netlist names these nodes `bl000` through `bl127`. Each column accumulates the programmed RRAM conductance contribution from the 128 wordline inputs.

The circuit drawing should show the following per-bitline path:

`RRAM bitline` → `Readout / I-to-V interface` → `BPF bank` → `Coherent-demodulation testbench` → `I/Q integrated outputs`

The readout block represents the observation interface that converts the bitline current-domain result into the voltage-domain signal used by the verification chain. The BPF bank separates the four carrier components associated with each bitline. The coherent-demodulation chain is implemented in the reusable verification testbench and produces the I/Q integrated outputs for each carrier.

## Block-Level Count

- Bitline nodes: 128
- Carrier components per bitline: 4
- Verification paths after BPF expansion: 512
- I/Q integrated outputs: 1024

## Figure-Level Wording

Use compact block labels that match the implementation:

- `Readout / I-to-V Interface`
- `BPF Bank`
- `Coherent-Demodulation Testbench`
- `I/Q Integration`

The diagram should keep the readout block aligned under each bitline or use a repeated-block notation with `×128`. The BPF and demodulation path can be shown as `×4 carriers / BL`, followed by `I/Q outputs`.
