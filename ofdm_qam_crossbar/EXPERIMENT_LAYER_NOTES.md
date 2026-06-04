# Experiment Layer Notes

This directory contains the algorithm-level inference-accuracy evaluation code
used to study carrier-domain non-idealities in neural-network inference.

The repository contains two complementary evaluation layers. This directory
focuses on neural-network inference behavior using PyTorch models. The
repository root contains the circuit-level RRAM crossbar verification flow,
including configuration files, generated netlists, reusable testbenches,
structural checks, result summaries, and review figures.

## Accuracy / Inference Evaluation

The inference-accuracy flow evaluates how carrier-domain demodulation
non-idealities affect neural-network accuracy at the algorithm level.

Relevant files:

- [`main_binary.py`](main_binary.py): training and evaluation entry point.
- [`evaluation202502/MODEM.py`](evaluation202502/MODEM.py): carrier-domain
  demodulation interference model.
- [`models/lenet5_with_mismatch_carrier_v2.py`](models/lenet5_with_mismatch_carrier_v2.py):
  LeNet-5 inference model with carrier mismatch injected after convolution
  layers.
- [`models/vgg_cifar10_with_mismatch_carrier_v2.py`](models/vgg_cifar10_with_mismatch_carrier_v2.py):
  VGG-style inference model with carrier mismatch injected after convolution
  layers.
- [`results_inference/`](results_inference/): lightweight inference logs and
  result files.

In this layer, the convolution output is treated as the ideal matrix-vector
multiplication result. The carrier-domain mismatch model perturbs this output
before the remaining neural-network layers continue inference.

## Binary Model Code

The directory also includes binary-network modules:

- [`models/binarized_modules.py`](models/binarized_modules.py)
- [`models/lenet5_binary.py`](models/lenet5_binary.py)
- [`models/vgg_cifar10_binary.py`](models/vgg_cifar10_binary.py)

These files implement binary weights and activations at the PyTorch model
level. They are used for neural-network evaluation and are separate from the
generated SPICE-level RRAM crossbar netlists.

## Circuit-Level RRAM Crossbar Verification

The circuit-level verification flow is stored at the repository root:

- [`../config/`](../config/): crossbar configuration and conductance matrices.
- [`../scripts/`](../scripts/): netlist generation, testbench generation,
  structural checks, result parsing, and performance extraction.
- [`../netlist/`](../netlist/): generated RRAM crossbar netlists.
- [`../tb/`](../tb/): reusable Spectre testbenches.
- [`../results/`](../results/): structural, sanity, BPF, and performance
  summaries.
- [`../review_package/`](../review_package/): visual and tabular evidence for
  design review.

The circuit-level flow verifies a generated 128 x 128 programmed read-state
RRAM crossbar. The generated conductance matrix uses binary Ron/Roff resistors
and an NMOS selector in each cell. The readout verification includes per-bitline
readout, BPF paths, coherent I/Q demodulation, integration, waveform exports,
and read-state performance extraction.

## Relationship Between the Two Layers

The inference-accuracy layer evaluates model-level robustness under
carrier-domain non-idealities. The circuit-level layer verifies that the
generated RRAM crossbar readout path is structurally consistent, executable in
Spectre, and measurable at the read-state level.

Together, the two layers provide complementary evidence: algorithm-level
inference behavior and circuit-level readout verification.
